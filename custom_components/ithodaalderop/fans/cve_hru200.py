"""Fan class for CVE/HRU200."""

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
    "Timer 10": "timer1",
    "Timer 20": "timer2",
    "Timer 30": "timer3",
}


def get_cve_hru200_fan(config_entry: ConfigEntry):
    """Create fan for CVE/HRU 200."""
    description = IthoFanEntityDescription(
        key="fan",
        supported_features=(
            FanEntityFeature.SET_SPEED
            | FanEntityFeature.PRESET_MODE
            | FanEntityFeature.TURN_ON
            | FanEntityFeature.TURN_OFF
        ),
        preset_modes=list(PRESET_MODES.keys()),
        command_topic=get_mqtt_command_topic(config_entry.data),
        state_topic=get_mqtt_state_topic(config_entry.data),
    )
    return [IthoFanCVE_HRU200(description, config_entry)]


class IthoFanCVE_HRU200(IthoBaseFan):
    """Representation of an MQTT-controlled fan."""

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""
        await mqtt.async_subscribe(
            self.hass, self.entity_description.state_topic, self._message_received, 1
        )

    @callback
    def _message_received(self, msg):
        """Handle preset mode update via MQTT."""
        data = json.loads(msg.payload)
        percentage = (
            int(data.get("Ventilation level (%)", -1))
            + int(data.get("Ventilation setpoint (%)", -1))
            + 1
        )
        if percentage >= 0:
            self._attr_percentage = percentage
        else:
            self._attr_percentage = None

        self.async_write_ha_state()

    async def async_set_preset_mode(self, preset_mode):
        """Set the fan preset mode."""
        if preset_mode in PRESET_MODES:
            preset_command = PRESET_MODES[preset_mode]
            await mqtt.async_publish(
                self.hass,
                self.entity_description.command_topic,
                preset_command,
            )
        else:
            _LOGGER.warning(f"Invalid preset mode: {preset_mode}")

    async def async_set_percentage(self, percentage: int) -> None:
        """Set the speed of the fan, as a percentage."""
        self._attr_percentage = percentage
        self.async_write_ha_state()

        await mqtt.async_publish(
            self.hass,
            self.entity_description.command_topic,
            int(percentage * 2.55),
        )

    async def async_turn_on(self, *args, **kwargs):
        """Turn on the fan."""
        await self.async_set_preset_mode("High")

    async def async_turn_off(self, **kwargs):
        """Turn off the fan."""
        await self.async_set_percentage(0)
