"""Sensor class for handling WPU sensors."""

import copy
import json

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from .const import MQTT_BASETOPIC, MQTT_STATETOPIC, WPU_STATUS
from .definitions.base import IthoSensorEntityDescription
from .definitions.wpu import WPU_ERROR_CODE_BYTE_TEMPLATE, WPU_SENSORS
from .sensor_base import IthoBaseSensor


def get_wpu_sensors(config_entry: ConfigEntry):
    """Create sensors for WPU."""
    sensors = []
    topic = f"{MQTT_BASETOPIC["wpu"]}/{MQTT_STATETOPIC["wpu"]}"
    for x in range(6):
        x = str(x)
        description = copy.deepcopy(WPU_ERROR_CODE_BYTE_TEMPLATE)
        description.topic = topic
        description.json_field = description.json_field + x
        description.translation_placeholders = {"num": x}
        description.unique_id = description.unique_id_template.replace("x", x)
        sensors.append(IthoSensorWPU(description, config_entry))

    for description in WPU_SENSORS:
        description.topic = topic
        sensors.append(IthoSensorWPU(description, config_entry))

    return sensors


class IthoSensorWPU(IthoBaseSensor):
    """Representation of Itho add-on sensor for WPU that is updated via MQTT."""

    def __init__(
        self,
        description: IthoSensorEntityDescription,
        config_entry: ConfigEntry,
    ) -> None:
        """Construct sensor for WPU."""
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
                value = payload[json_field]
                if json_field == "Status":
                    self._extra_state_attributes = {
                        "Code": value,
                    }
                    value = WPU_STATUS.get(int(value), "Unknown status")
                if json_field == "ECO selected on thermostat":
                    if value == 1:
                        value = "Eco"
                    if payload["Comfort selected on thermostat"] == 1:
                        value = "Comfort"
                    if payload["Boiler boost from thermostat"] == 1:
                        value = "Boost"
                    if payload["Boiler blocked from thermostat"] == 1:
                        value = "Off"
                    if payload["Venting from thermostat"] == 1:
                        value = "Venting"

            self._attr_native_value = value
            self.async_write_ha_state()

        await mqtt.async_subscribe(
            self.hass, self.entity_description.topic, message_received, 1
        )
