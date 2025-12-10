"""Fan class for Demandflow."""

import json

from homeassistant.components import mqtt
from homeassistant.components.fan import FanEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ..const import _LOGGER, MQTT_DEFAULT_QOS_PUBLISH, MQTT_DEFAULT_QOS_SUBSCRIBE
from ..definitions.base_definitions import IthoFanEntityDescription
from ..utils import get_mqtt_command_topic, get_mqtt_state_topic
from .base_fans import IthoBaseFan

PRESET_MODES = {
    "Low": "low",
    "High": "high",
    "Cook 30": "cook30",
    "Cook 60": "cook60",
    "Timer 10": "timer1",
    "Timer 20": "timer2",
    "Timer 30": "timer3",
}

ACTUAL_MODES = {
    "status-normal": "Normal",
    "status-eco-comfort": "Eco Comfort",
    "status-timer": "Timer",
    "status-high-extractor-hood": "High Extractor Hood",
    "status-high-extractor-hood-and-bathr": "High Extractor Hood and Bathroom",
}


def get_df_fan(config_entry: ConfigEntry):
    """Create fan for Demandflow."""
    description = IthoFanEntityDescription(
        key="fan",
        supported_features=(
            FanEntityFeature.PRESET_MODE
            | FanEntityFeature.TURN_ON
            | FanEntityFeature.TURN_OFF
        ),
        preset_modes=list(PRESET_MODES.keys()),
        command_topic=get_mqtt_command_topic(config_entry.data),
        command_key="vremotecmd",
        state_topic=get_mqtt_state_topic(config_entry.data),
    )
    return [IthoFanDF(description, config_entry)]


class IthoFanDF(IthoBaseFan):
    """Representation of an MQTT-controlled fan."""

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""
        await mqtt.async_subscribe(
            self.hass,
            self.entity_description.state_topic,
            self._message_received,
            MQTT_DEFAULT_QOS_SUBSCRIBE,
        )

    @callback
    def _message_received(self, msg):
        """Handle preset mode update via MQTT."""
        data = json.loads(msg.payload)

        if int(data.get("status-normal", -1)) == 1:
            self._attr_preset_mode = "Low"
        else:
            self._attr_preset_mode = "High"

        self.async_write_ha_state()

    async def async_set_preset_mode(self, preset_mode):
        """Set the fan preset mode."""
        if preset_mode in PRESET_MODES:
            self._attr_preset_mode = preset_mode
            self.async_write_ha_state()

            preset_command = PRESET_MODES[preset_mode]
            payload = json.dumps({self.entity_description.command_key: preset_command})
            await mqtt.async_publish(
                self.hass,
                self.entity_description.command_topic,
                payload,
                MQTT_DEFAULT_QOS_PUBLISH,
            )
        else:
            _LOGGER.warning(f"Invalid preset mode: {preset_mode}")

    async def async_turn_on(self, *args, **kwargs):
        """Turn on the fan."""
        await self.async_set_preset_mode("Cook 30") #Default turn on

    async def async_turn_off(self, **kwargs):
        """Turn off the fan."""
        await self.async_set_preset_mode("Low")

    @property
    def is_on(self):
        """Return true if the fan is on."""
        return self._attr_preset_mode == "High"