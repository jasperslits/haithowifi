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
    CONF_ENTITIES_CREATION_MODE,
    CONF_NONCVE_MODEL,
    DOMAIN,
    MANUFACTURER,
    MQTT_BASETOPIC,
    MQTT_STATETOPIC,
    NONCVE_DEVICES,
)
from .definitions.base import IthoBinarySensorEntityDescription
from .definitions.cve import CVE_BINARY_SENSORS
from .definitions.hru350 import HRU_ECO_350_BINARY_SENSORS
from .definitions.hrueco import HRU_ECO_BINARY_SENSORS
from .definitions.wpu import WPU_BINARY_SENSORS


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
    selected_sensors = []
    if config_entry.data[CONF_ADDON_TYPE] == "cve":
        for description in CVE_BINARY_SENSORS:
            description.topic = f"{MQTT_BASETOPIC["cve"]}/{MQTT_STATETOPIC["cve"]}"
            sensors.append(IthoBinarySensor(description, config_entry))

    if config_entry.data[CONF_ADDON_TYPE] == "noncve" and config_entry.data[
        CONF_NONCVE_MODEL
    ] in ["hru_eco", "hru_eco_350"]:
        if config_entry.data[CONF_NONCVE_MODEL] == "hru_eco":
            hru_sensors = HRU_ECO_BINARY_SENSORS
        if config_entry.data[CONF_NONCVE_MODEL] == "hru_eco_350":
            hru_sensors = HRU_ECO_350_BINARY_SENSORS

        for description in hru_sensors:
            description.topic = (
                f"{MQTT_BASETOPIC["noncve"]}/{MQTT_STATETOPIC["noncve"]}"
            )
            sensors.append(IthoBinarySensor(description, config_entry))

    if config_entry.data[CONF_ADDON_TYPE] == "wpu":
        for description in WPU_BINARY_SENSORS:
            description.topic = f"{MQTT_BASETOPIC["wpu"]}/{MQTT_STATETOPIC["wpu"]}"
            sensors.append(IthoBinarySensor(description, config_entry))

    for sensor in sensors:
        if (
            config_entry.data[CONF_ENTITIES_CREATION_MODE] == "only_selected"
            and not sensor.entity_description.is_selected_entity
        ):
            continue
        selected_sensors.append(sensor)

    async_add_entities(selected_sensors)


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
        self.entity_description.translation_key = self.entity_description.key

        model = ADDON_TYPES[config_entry.data[CONF_ADDON_TYPE]]
        if config_entry.data[CONF_ADDON_TYPE] == "noncve":
            model = f"{model} - {NONCVE_DEVICES[config_entry.data[CONF_NONCVE_MODEL]]}"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.data[CONF_ADDON_TYPE])},
            manufacturer=MANUFACTURER,
            model=model,
            name=f"Itho Daalderop {ADDON_TYPES[config_entry.data[CONF_ADDON_TYPE]]}",
        )

        self._attr_unique_id = (
            f"itho_{ADDON_TYPES[config_entry.data[CONF_ADDON_TYPE]]}_{description.key}"
        )
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
            json_field = self.entity_description.json_field
            if json_field not in payload:
                value = None
            else:
                value = bool(payload[json_field])

            self._attr_is_on = value
            self.async_write_ha_state()

        await mqtt.async_subscribe(
            self.hass, self.entity_description.topic, message_received, 1
        )
