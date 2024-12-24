"""Sensor class for handling Last Command sensors."""

import json

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from .const import CONF_ADDON_TYPE, MQTT_BASETOPIC, MQTT_STATETOPIC
from .definitions.base import IthoSensorEntityDescription
from .definitions.last_command import LAST_CMD_SENSORS
from .sensor_base import IthoBaseSensor


def get_last_command_sensors(config_entry: ConfigEntry):
    """Create sensors for Last Command."""
    sensors = []
    topic = f"{MQTT_BASETOPIC[config_entry.data[CONF_ADDON_TYPE]]}/{MQTT_STATETOPIC["last_cmd"]}"
    for description in LAST_CMD_SENSORS:
        description.topic = topic
        sensors.append(IthoSensorLastCommand(description, config_entry))

    return sensors


class IthoSensorLastCommand(IthoBaseSensor):
    """Representation of Itho add-on sensor for Last Command that is updated via MQTT."""

    def __init__(
        self, description: IthoSensorEntityDescription, config_entry: ConfigEntry
    ) -> None:
        """Construct sensor for Last Command."""
        super().__init__(description, config_entry)

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""

        @callback
        def message_received(message):
            """Handle new MQTT messages."""
            payload = json.loads(message.payload)
            value = payload.get(self.entity_description.json_field, None)

            self._attr_native_value = value
            self.async_write_ha_state()

        await mqtt.async_subscribe(
            self.hass, self.entity_description.topic, message_received, 1
        )
