"""Climate entities for AutoTemp rooms and the Itho Spiders that control them."""

from collections.abc import Mapping
from functools import lru_cache
import json
import math
import time
from typing import Any

from homeassistant.components import mqtt
from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_call_later
from homeassistant.util import slugify

from .const import (
    _LOGGER,
    CONF_ADDON_TYPE,
    DOMAIN,
    MQTT_DEFAULT_QOS_PUBLISH,
    MQTT_DEFAULT_QOS_SUBSCRIBE,
)
from .utils import (
    get_device_info,
    get_entity_prefix,
    get_mqtt_command_topic,
    get_mqtt_remote_topic,
    get_mqtt_state_topic,
    get_room_device_info,
    get_rooms,
)

SEND_DELAY = 3  # seconds to wait for more +/- presses before sending
PENDING_TIMEOUT = 16 * 60  # the add-on retries a setpoint for 15 minutes
DROP_GRACE = 30  # seconds before a different setpoint_cmd counts as dropped
ACTION_HOLD = 3 * 60  # seconds heating/cooling stays shown; valves close slowly
SYSTEM_STATES = {
    "state hand": "hand",
    "State heating": "heating",
    "State cool": "cooling",
    "State off": "off",
}
ACTIONS = {"heating": HVACAction.HEATING, "cooling": HVACAction.COOLING}
MODES = {HVACAction.HEATING: HVACMode.HEAT, HVACAction.COOLING: HVACMode.COOL}


@lru_cache(maxsize=8)
def _load(raw: str | bytes) -> dict | None:
    """Parse a message once for all entities; the result must not be changed."""
    try:
        data = json.loads(raw)
    except ValueError:
        return None
    return data if isinstance(data, dict) else None


def _num(value: Any) -> float | None:
    ok = isinstance(value, int | float) and not isinstance(value, bool)
    return float(value) if ok and math.isfinite(value) else None


def _first(*values):
    return next((value for value in values if value is not None), None)


def _same(a: float | None, b: float | None) -> bool:
    return a is not None and b is not None and abs(a - b) < 0.05


def _norm(name: str) -> str:
    """Normalize a name like the config flow does."""
    return name.replace(" ", "_")


def _is_spider(caps: Any) -> bool:
    return isinstance(caps, dict) and "temp" in caps and "setpoint" in caps


def _spider_id(data: Mapping[str, Any], spider: str) -> str:
    return f"{get_entity_prefix(data)}_spider_{slugify(spider)}".lower()


def _action(system: str | None, power, temp, setpoint, cool) -> HVACAction:
    """Get what a room is doing: its AutoTemp power, else the temperature demand."""
    if system == "off":
        return HVACAction.OFF
    if power is not None:
        return ACTIONS.get(system, HVACAction.IDLE) if power > 0 else HVACAction.IDLE
    wanted = HVACAction.IDLE
    if None not in (temp, setpoint) and temp < setpoint:
        wanted = HVACAction.HEATING
    elif None not in (temp, cool) and temp > cool:
        wanted = HVACAction.COOLING
    return wanted if system in (None, wanted) else HVACAction.IDLE


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Create a thermostat per room and one per Spider that has no room."""
    data = entry.data
    if not await mqtt.async_wait_for_mqtt_client(hass):
        _LOGGER.error("MQTT integration is not available")
        return

    # A Spider can be joined to another add-on than the room it controls.
    configs = [
        other.data
        for other in hass.config_entries.async_entries(
            DOMAIN, include_ignore=False, include_disabled=False
        )
    ]
    commands = {get_mqtt_remote_topic(c): get_mqtt_command_topic(c) for c in configs}
    linked = {_norm(s) for c in configs for _, s in get_rooms(c).values() if s}
    registry = er.async_get(hass)
    for spider in linked:
        unique_id = _spider_id(data, spider)
        if entity_id := registry.async_get_entity_id("climate", DOMAIN, unique_id):
            registry.async_remove(entity_id)

    async_add_entities(
        Thermostat(data, commands, room=number, name=room, spider=spider)
        for number, (room, spider) in get_rooms(data).items()
    )

    topic = get_mqtt_remote_topic(data)
    own = {topic: commands[topic]}
    known: set[str] = set()

    @callback
    def on_remotes(msg: mqtt.ReceiveMessage) -> None:
        new = []
        for key, caps in (_load(msg.payload) or {}).items():
            uid = _spider_id(data, key)
            if uid not in known and _is_spider(caps) and _norm(key) not in linked:
                known.add(uid)
                new.append(Thermostat(data, own, spider=key, initial=msg))
        if new:
            async_add_entities(new)

    entry.async_on_unload(
        await mqtt.async_subscribe(hass, topic, on_remotes, MQTT_DEFAULT_QOS_SUBSCRIBE)
    )


class Thermostat(ClimateEntity):
    """Thermostat of an AutoTemp room and/or the Spider that controls it."""

    _attr_has_entity_name = True
    _attr_should_poll = False
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_hvac_modes = [HVACMode.OFF, HVACMode.HEAT, HVACMode.COOL]
    _attr_min_temp = 5.0
    _attr_max_temp = 30.0
    _attr_target_temperature_step = 0.5

    def __init__(
        self,
        data: Mapping[str, Any],
        commands: dict[str, str],
        *,
        room: int | None = None,
        name: str = "",
        spider: str = "",
        initial: mqtt.ReceiveMessage | None = None,
    ) -> None:
        """Initialize a room thermostat, or a Spider thermostat without a room."""
        self._room = room
        self._link = _norm(spider)  # empty without a Spider
        self._commands = commands  # remotesinfo topic -> command topic
        autotemp = data[CONF_ADDON_TYPE] == "autotemp"
        self._status_topic = get_mqtt_state_topic(data) if autotemp else None
        self._status: dict | None = None
        self._spider: dict | None = None
        self._topic: str | None = None  # remotesinfo topic of the Spider's add-on
        self._index = 0
        self._held = (HVACAction.IDLE, 0.0)  # last heating/cooling and its expiry
        self._pending: float | None = None  # requested, not yet confirmed
        self._sent: float | None = None  # monotonic time the command was sent
        self._cancel_send = None
        if room is None:
            self._attr_name = spider
            self._attr_device_info = get_device_info(data)
            self._attr_unique_id = _spider_id(data, spider)
            self.entity_id = f"climate.{self._attr_unique_id}"
        else:
            self._attr_name = None
            self._attr_device_info = get_room_device_info(data, name)
            prefix = get_entity_prefix(data)
            self._attr_unique_id = f"{prefix}_room_{name}_climate".lower()
        if initial is not None:
            self._on_remotes(initial)
        else:
            self._refresh()

    def _refresh(self) -> None:
        status, spider, room = self._status, self._spider, self._room
        caps = spider or {}
        room_temp = room_setp = power = system = None
        if status is not None:
            system = next(
                (v for k, v in SYSTEM_STATES.items() if status.get(k) == 1), "idle"
            )
            if room is not None:
                room_temp, room_setp, *powers = (
                    _num(status.get(f"Room {room} {key}"))
                    for key in ("temp", "setp", "power % (%)", "power kW (kW)")
                )
                power = max((p for p in powers if p is not None), default=None)
        temp, setpoint, cool, cmd = (
            _num(caps.get(key))
            for key in ("temp", "setpoint", "setpoint_cool", "setpoint_cmd")
        )
        active = _first(room_setp, setpoint)  # the AutoTemp's setting is in force
        now = time.monotonic()

        if spider is None:
            self._pending = None
        elif self._pending is not None and self._sent is not None:
            waited = now - self._sent
            dropped = waited > DROP_GRACE and cmd is not None
            if (
                _same(active, self._pending)
                or (dropped and not _same(cmd, self._pending))
                or waited > PENDING_TIMEOUT
            ):
                self._pending = None  # in force, dropped by the add-on or timed out

        # The AutoTemp and Spider both lag, so keep heating/cooling for a while.
        action = _action(
            system, power, _first(room_temp, temp), _first(setpoint, room_setp), cool
        )
        if action in MODES:
            self._held = (action, now + ACTION_HOLD)
        elif action == HVACAction.OFF:
            self._held = (HVACAction.IDLE, 0.0)
        elif now < self._held[1]:
            action = self._held[0]

        pending = self._pending
        if pending is None:
            text = "read only" if spider is None else "applied"
        elif active is None:
            text = "waiting for Spider"
        else:
            text = f"waiting for Spider (now {active} °C)"
        self._attr_available = spider is not None or (
            status is not None and room is not None
        )
        self._attr_supported_features = (
            ClimateEntityFeature(0)
            if spider is None
            else ClimateEntityFeature.TARGET_TEMPERATURE
        )
        self._attr_current_temperature = _first(room_temp, temp)
        self._attr_target_temperature = _first(pending, active)
        self._attr_hvac_action = action
        self._attr_hvac_mode = MODES.get(action, HVACMode.OFF)
        self._attr_icon = None if pending is None else "mdi:timer-sand"
        self._attr_extra_state_attributes = {
            "setpoint_status": text,
            "pending_setpoint": pending,
            "active_setpoint": active,
            "spider_setpoint": setpoint,
            "setpoint_cool": cool,
            "system_state": system,
            "battery": _num(caps.get("battery")),
            "presence": bool(caps["pir"]) if "pir" in caps else None,
        }
        if self.hass is not None:
            self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """Subscribe to the AutoTemp status and, if linked, to the Spider's add-ons."""
        topics = {self._status_topic: self._on_status} if self._status_topic else {}
        if self._link:
            topics |= dict.fromkeys(self._commands, self._on_remotes)
        for topic, handler in topics.items():
            self.async_on_remove(
                await mqtt.async_subscribe(
                    self.hass, topic, handler, MQTT_DEFAULT_QOS_SUBSCRIBE
                )
            )

    @callback
    def _on_status(self, msg: mqtt.ReceiveMessage) -> None:
        if (status := _load(msg.payload)) is not None:
            self._status = status
            self._refresh()

    @callback
    def _on_remotes(self, msg: mqtt.ReceiveMessage) -> None:
        if (payload := _load(msg.payload)) is None:
            return
        if self._topic in (None, msg.topic):  # keep the first add-on reporting it
            found = (  # the index is the Spider's slot in the add-on
                (index, caps, msg.topic)
                for index, (key, caps) in enumerate(payload.items())
                if _norm(key) == self._link and _is_spider(caps)
            )
            self._index, self._spider, self._topic = next(found, (0, None, None))
        self._refresh()

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Send the setpoint once the +/- presses stop."""
        temperature = _num(kwargs.get(ATTR_TEMPERATURE))
        if temperature is None or self._spider is None:
            return
        self._pending, self._sent = temperature, None
        self._refresh()
        if self._cancel_send:
            self._cancel_send()
        self._cancel_send = async_call_later(self.hass, SEND_DELAY, self._send)

    async def _send(self, _now) -> None:
        self._cancel_send = None
        if self._pending is None or self._topic is None:
            return
        self._sent = time.monotonic()
        await mqtt.async_publish(
            self.hass,
            self._commands[self._topic],
            json.dumps({"rfsetpoint": self._pending, "rfremoteindex": self._index}),
            MQTT_DEFAULT_QOS_PUBLISH,
        )
        self._refresh()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Reject mode changes; the mode follows what the room is doing."""
        raise ServiceValidationError("The mode follows the AutoTemp and cannot be set")

    async def async_will_remove_from_hass(self) -> None:
        """Cancel a scheduled send."""
        if self._cancel_send:
            self._cancel_send()
