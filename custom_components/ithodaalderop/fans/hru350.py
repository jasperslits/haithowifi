"""Fan class for HRU 350 Eco."""

import json

from homeassistant.components import mqtt
from homeassistant.components.fan import FanEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ..const import _LOGGER
from ..definitions.base import IthoFanEntityDescription
from .base import IthoBaseFan

MQTT_COMMAND_TOPIC = "cmd"

PRESET_MODES = {
    "Low": "low",
    "Medium": "medium",
    "High": "high",
    "Auto": "auto",
    "Autonight": "autonight",
    "Timer 10": "timer1",
    "Timer 20": "timer2",
    "Timer 30": "timer3",
    "Timer": "timer",
}

ACTUAL_MODES = {
    1: "Low",
    2: "Medium",
    3: "High",
    13: "Timer",
    24: "Auto",
    25: "Autonight",
}

ENTITY_DESCRIPTION = IthoFanEntityDescription(
    key="fan",
    supported_features=FanEntityFeature.PRESET_MODE
    | FanEntityFeature.TURN_ON
    | FanEntityFeature.TURN_OFF,
    preset_modes=list(PRESET_MODES.keys()),
)


def get_hru350_fan(config_entry: ConfigEntry):
    """Create fan for HRU 350 Eco."""
    return [IthoFanHRU350(ENTITY_DESCRIPTION, config_entry)]


class IthoFanHRU350(IthoBaseFan):
    """Representation of an MQTT-controlled fan."""

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""
        await mqtt.async_subscribe(
            self.hass, "ithohru/ithostatus", self._message_received, 1
        )

    @callback
    def _message_received(self, msg):
        """Handle preset mode update via MQTT."""
        try:
            data = json.loads(msg.payload)
            actual_mode = int(data.get("Actual Mode", -1))

            if actual_mode in ACTUAL_MODES:
                self._preset_mode = ACTUAL_MODES[actual_mode]
            else:
                _LOGGER.error("Invalid actual mode: %s", actual_mode)

            self.async_write_ha_state()
        except ValueError:
            _LOGGER.error("Invalid JSON received for preset mode: %s", msg.payload)

    async def async_set_preset_mode(self, preset_mode):
        """Set the fan preset mode."""
        if preset_mode in PRESET_MODES:
            preset_command = PRESET_MODES[preset_mode]

            payload = json.dumps({"vremotecmd": preset_command})
            await mqtt.async_publish(
                self.hass, f"ithohru/{MQTT_COMMAND_TOPIC}", payload
            )
            self._preset_mode = preset_mode
            self.async_write_ha_state()
        else:
            _LOGGER.warning("Invalid preset mode: %s", preset_mode)

    async def async_turn_on(self, *args, **kwargs):
        """Turn on the fan."""
        await self.async_set_preset_mode("Auto")

    async def async_turn_off(self, **kwargs):
        """Turn off the fan."""
        await self.async_set_preset_mode("Low")

    @property
    def is_on(self):
        """Return true if the fan is on."""
        return self._preset_mode is not None and self._preset_mode != "Low"
