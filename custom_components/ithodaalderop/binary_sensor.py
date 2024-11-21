#!/usr/bin/env python3
"""Binary Sensor component for Itho.

Author: Benjamin
"""

import json

from homeassistant.components import mqtt
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    _LOGGER,
    ADDON_TYPES,
    CONF_ADDON_TYPE,
    DOMAIN,
    MANUFACTURER,
    MQTT_BASETOPIC,
    MQTT_STATETOPIC,
)
from .definitions import (
    AUTOTEMPBINARYSENSORS,
    NONCVEBINARYSENSORS,
    IthoBinarySensorEntityDescription,
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Itho add-on binary sensors from config entry based on their type."""

    if not await mqtt.async_wait_for_mqtt_client(hass):
        _LOGGER.error("MQTT integration is not available")
        return

    sensors = []
    if config_entry.data[CONF_ADDON_TYPE] == "noncve":
        for description in NONCVEBINARYSENSORS:
            description.key = f"{MQTT_BASETOPIC["noncve"]}/{MQTT_STATETOPIC["noncve"]}"
            sensors.append(IthoBinarySensor(description, config_entry))

    if config_entry.data[CONF_ADDON_TYPE] == "autotemp":
        for description in AUTOTEMPBINARYSENSORS:
            description.key = f"{MQTT_BASETOPIC["autotemp"]}/{MQTT_STATETOPIC["autotemp"]}"
            sensors.append(IthoBinarySensor(description, config_entry))

    async_add_entities(sensors)


class IthoBinarySensor(BinarySensorEntity):
    """Representation of a Itho add-on binary sensor that is updated via MQTT."""

    _attr_has_entity_name = True
    entity_description: IthoBinarySensorEntityDescription

    def __init__(
        self,
        description: IthoBinarySensorEntityDescription,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the binary sensor."""
        self.entity_description = description

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.data[CONF_ADDON_TYPE])},
            manufacturer=MANUFACTURER,
            model=ADDON_TYPES[config_entry.data[CONF_ADDON_TYPE]],
            name="Itho Daalderop " + ADDON_TYPES[config_entry.data[CONF_ADDON_TYPE]],
        )

        self._attr_unique_id = f"itho_{ADDON_TYPES[config_entry.data[CONF_ADDON_TYPE]]}_{description.translation_key}"
        self.entity_id = f"binary_sensor.{self._attr_unique_id}"

    @property
    def icon(self):
        """Icon for binary sensor."""
        if (
            self.entity_description.icon_off is not None
            and self.entity_description.icon_on is not None
        ):
            if self._attr_is_on:
                return self.entity_description.icon_on
            return self.entity_description.icon_off
        if self.entity_description.icon is not None:
            return self.entity_description.icon
        return None

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""

        @callback
        def message_received(message):
            """Handle new MQTT messages."""
            payload = json.loads(message.payload)
            if self.entity_description.json_field not in payload:
                value = None
            else:
                value = bool(payload[self.entity_description.json_field])

            self._attr_is_on = value
            self.async_write_ha_state()

        await mqtt.async_subscribe(
            self.hass, self.entity_description.key, message_received, 1
        )
