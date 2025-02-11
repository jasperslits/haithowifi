"""Fan class for HRU 350 Eco."""

import json

from homeassistant.components import mqtt
from homeassistant.components.fan import FanEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ..const import _LOGGER
from ..definitions.base_definitions import IthoFanEntityDescription
from ..utils import get_mqtt_command_topic, get_mqtt_state_topic
from .base_fans import IthoBaseFan

PRESET_MODES = {
    "Low": "low",
    "Medium": "medium",
    "High": "high",
    "Auto": "auto",
    "Timer 10": "timer1",
    "Timer 20": "timer2",
    "Timer 30": "timer3",
}

COMMAND_KEY = "rfremotecmd"


def get_hru250_300_fan(config_entry: ConfigEntry):
    """Create fan for HRU 250/300."""
    description = IthoFanEntityDescription(
        key="fan",
        supported_features=(
            FanEntityFeature.PRESET_MODE
            | FanEntityFeature.TURN_ON
            | FanEntityFeature.TURN_OFF
        ),
        preset_modes=list(PRESET_MODES.keys()),
        command_topic=get_mqtt_command_topic(config_entry.data),
        state_topic=get_mqtt_state_topic(config_entry.data),
    )
    return [IthoFanHRU250_300(description, config_entry)]


class IthoFanHRU250_300(IthoBaseFan):
    """Representation of an MQTT-controlled fan."""

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""
        await mqtt.async_subscribe(
            self.hass, self.entity_description.state_topic, self._message_received, 1
        )

    @callback
    def _message_received(self, msg):
        """Handle preset mode update via MQTT."""
        try:
            data = json.loads(msg.payload)
            speed = int(data.get("Absolute speed of the fan (%)", -1))

            if speed >= 90:
                self._preset_mode = "High"
            elif speed >= 40:
                self._preset_mode = "Medium"
            elif speed >= 0:
                self._preset_mode = "Low"
            else:
                self._preset_mode = None

            self.async_write_ha_state()
        except ValueError:
            _LOGGER.error("Invalid JSON received for preset mode: %s", msg.payload)

    async def async_set_preset_mode(self, preset_mode):
        """Set the fan preset mode."""
        if preset_mode in PRESET_MODES:
            preset_command = PRESET_MODES[preset_mode]

            payload = json.dumps({COMMAND_KEY: preset_command})
            await mqtt.async_publish(
                self.hass,
                self.entity_description.command_topic,
                payload,
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
