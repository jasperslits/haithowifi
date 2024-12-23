"""Sensor class for handling WPU sensors."""

import json

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ._sensor_base import IthoBaseSensor
from .const import WPU_STATUS
from .definitions.base import IthoSensorEntityDescription


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
            self.hass, self.entity_description.key, message_received, 1
        )
