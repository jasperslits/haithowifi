"""Sensor class for handling CO2 Remote sensors."""

import copy
import json

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ..const import CONF_ADDON_TYPE, MQTT_BASETOPIC, MQTT_STATETOPIC
from ..definitions.co2_remote import REMOTE_SENSOR_TEMPLATE
from .base import IthoBaseSensor


def get_co2_remote_sensors(config_entry: ConfigEntry):
    """Create remotes for CO2 monitoring."""
    sensors = []
    topic = f"{MQTT_BASETOPIC[config_entry.data[CONF_ADDON_TYPE]]}/{MQTT_STATETOPIC["remote"]}"
    for x in range(1, 5):
        remote = config_entry.data["remote" + str(x)]
        if remote not in ("", "Remote " + str(x)):
            description = copy.deepcopy(REMOTE_SENSOR_TEMPLATE)
            description.topic = topic
            description.json_field = remote
            description.translation_placeholders = {"remote_name": remote}
            description.unique_id = remote
            sensors.append(IthoSensorCO2Remote(description, config_entry))

    return sensors


class IthoSensorCO2Remote(IthoBaseSensor):
    """Representation of Itho add-on sensor for a Remote that is updated via MQTT."""

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""
        await mqtt.async_subscribe(
            self.hass, self.entity_description.topic, self.message_received, 1
        )

    @callback
    def message_received(self, message):
        """Handle new MQTT messages."""
        payload = json.loads(message.payload)
        json_field = self.entity_description.json_field
        if json_field not in payload:
            value = None
        else:
            value = payload[json_field]["co2"]

        self._attr_native_value = value
        self.async_write_ha_state()
