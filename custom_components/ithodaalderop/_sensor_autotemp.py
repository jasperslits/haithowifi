"""Sensor class for handling Autotemp sensors."""

import json

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo

from ._sensor_base import IthoBaseSensor
from .const import (
    ADDON_TYPES,
    AUTOTEMP_ERROR,
    AUTOTEMP_MODE,
    CONF_ADDON_TYPE,
    DOMAIN,
    MANUFACTURER,
)
from .definitions.base import IthoSensorEntityDescription


class IthoSensorAutotemp(IthoBaseSensor):
    """Representation of Itho add-on sensor for Autotemp data that is updated via MQTT."""

    def __init__(
        self,
        description: IthoSensorEntityDescription,
        config_entry: ConfigEntry,
    ) -> None:
        """Construct sensor for Autotemp."""
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
                if json_field == "Error":
                    self._extra_state_attributes = {
                        "Code": value,
                    }
                    value = AUTOTEMP_ERROR.get(value, "Unknown error")

                if json_field == "Mode":
                    self._extra_state_attributes = {
                        "Code": value,
                    }
                    value = AUTOTEMP_MODE.get(value, "Unknown mode")

                if json_field == "State off":
                    if value == 1:
                        value = "Off"
                    if payload["State cool"] == 1:
                        value = "Cooling"
                    if payload["State heating"] == 1:
                        value = "Heating"
                    if payload["state hand"] == 1:
                        value = "Hand"

            self._attr_native_value = value
            self.async_write_ha_state()

        await mqtt.async_subscribe(
            self.hass, self.entity_description.key, message_received, 1
        )


class IthoSensorAutotempRoom(IthoBaseSensor):
    """Representation of Itho add-on room sensor for Autotemp data that is updated via MQTT."""

    def __init__(
        self, description: IthoSensorEntityDescription, config_entry: ConfigEntry
    ) -> None:
        """Construct sensor for Autotemp."""

        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    DOMAIN,
                    f"{config_entry.data[CONF_ADDON_TYPE]}_room_{description.room.lower()}",
                )
            },
            manufacturer=MANUFACTURER,
            model=f"{ADDON_TYPES[config_entry.data[CONF_ADDON_TYPE]]} Spider",
            name=f"Spider {description.room.capitalize()}",
            via_device=(DOMAIN, config_entry.data[CONF_ADDON_TYPE]),
        )

        super().__init__(description, config_entry, use_base_sensor_device=False)

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
            self.hass, self.entity_description.key, message_received, 1
        )
