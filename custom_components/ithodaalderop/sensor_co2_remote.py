"""Sensor class for handling CO2 Remote sensors."""

import json

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from .definitions.base import IthoSensorEntityDescription
from .sensor_base import IthoBaseSensor


class IthoSensorCO2Remote(IthoBaseSensor):
    """Representation of Itho add-on sensor for a Remote that is updated via MQTT."""

    def __init__(
        self,
        description: IthoSensorEntityDescription,
        config_entry: ConfigEntry,
    ) -> None:
        """Construct sensor for Remote."""
        super().__init__(description, config_entry)

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""

        @callback
        def message_received(message):
            """Handle new MQTT messages."""
            payload = json.loads(message.payload)
            json_field = self.entity_description.json_field
            if json_field not in payload:
                value = None
            else:
                value = payload[json_field]["co2"]

            self._attr_native_value = value
            self.async_write_ha_state()

        await mqtt.async_subscribe(
            self.hass, self.entity_description.topic, message_received, 1
        )
