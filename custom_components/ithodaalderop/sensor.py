#!/usr/bin/env python3
"""
Sensor component for Itho
Author: Jasper Slits
"""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components import mqtt
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant, callback

import json
import copy
from .const import *
from .const import _LOGGER
from .definitions import CVESENSORS, NONCVESENSORS, WPUSENSORS, AUTOTEMPSENSORS, IthoSensorEntityDescription


def _create_remotes(config_entry: ConfigEntry):

    cfg = config_entry.data

    if cfg[CONF_REMOTE_1] != "":
        REMOTES = [
            IthoSensorEntityDescription(
                json_field=cfg[CONF_REMOTE_1],
                key=MQTT_STATETOPIC["remotes"],
                translation_key=cfg[CONF_REMOTE_1],
                device_class="carbon_dioxide",
                native_unit_of_measurement="ppm",
                state_class="measurement")]

    if cfg[CONF_REMOTE_2] != "":
        REMOTES.append(
            IthoSensorEntityDescription(
                json_field=cfg[CONF_REMOTE_2],
                key=MQTT_STATETOPIC["remotes"],
                translation_key=cfg[CONF_REMOTE_2],
                device_class="carbon_dioxide",
                native_unit_of_measurement="ppm",
                state_class="measurement"))

    return REMOTES


def _create_autotemprooms(config_entry: ConfigEntry):
    cfg = config_entry.data
    configured_sensors = []
    for x in range(1, 8):
        template_sensors = copy.deepcopy(list(AUTOTEMPSENSORS))
        room = cfg["room" + str(x)]
        if room != "":
            for sensor in template_sensors:
                sensor.json_field = sensor.json_field.replace("X", str(x))
                sensor.translation_key = sensor.translation_key.replace("X", room)
                configured_sensors.append(sensor)

    return configured_sensors


async def async_setup_entry(
    _: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Itho add-on sensors from config entry based on their type."""
    if config_entry.data[CONF_CVE_TYPE] == "noncve":
        async_add_entities(IthoSensor(description, config_entry, AddOnType.NONCVE) for description in NONCVESENSORS)
    if config_entry.data[CONF_CVE_TYPE] == "cve":
        async_add_entities(IthoSensor(description, config_entry, AddOnType.CVE) for description in CVESENSORS)
    if config_entry.data[CONF_USE_WPU]:
        async_add_entities(IthoSensor(description, config_entry, AddOnType.WPU) for description in WPUSENSORS)
    if config_entry.data[CONF_USE_REMOTES]:
        async_add_entities(IthoSensor(description, config_entry, AddOnType.REMOTES) for description in _create_remotes(config_entry))
    if config_entry.data[CONF_USE_AUTOTEMP]:
        async_add_entities(IthoSensor(description, config_entry, AddOnType.AUTOTEMP) for description in _create_autotemprooms(config_entry))


class IthoSensor(SensorEntity):
    """Representation of a Itho add-on sensor that is updated via MQTT."""

    _attr_has_entity_name = True
    entity_description: IthoSensorEntityDescription

    def __init__(
        self, description: IthoSensorEntityDescription, config_entry: ConfigEntry, aot: AddOnType
    ) -> None:
        """Initialize the sensor."""
        self.entity_description = description

        self.entity_id = f"sensor.{ADDONS[aot].lower()}_{description.translation_key}"
        self._attr_unique_id = f"{config_entry.entry_id}-{description.translation_key}"
        self.aot = aot

    @property
    def name(self):
        return self.entity_description.translation_key.replace("_", " ").capitalize()

    @property
    def icon(self):
        if self.entity_description.native_unit_of_measurement in UNITTYPE_ICONS:
            return UNITTYPE_ICONS[self.entity_description.native_unit_of_measurement]

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""

        @callback
        def message_received(message):
            """Handle new MQTT messages."""
            if message.payload == "":
                self._attr_native_value = None
            elif self.entity_description.state is not None:
                self._attr_native_value = self.entity_description.state(message.payload)
            else:
                payload = json.loads(message.payload)
                if self.entity_description.json_field not in payload:
                    value = None
                else:
                    value = payload[self.entity_description.json_field]
                    if self.aot == AddOnType.NONCVE and self.entity_description.json_field == "Actual Mode":
                        value = HRU_ACTUAL_MODE[value]

                    if self.aot == AddOnType.WPU and self.entity_description.json_field == "Status":
                        value = WPU_STATUS[value]

                    if self.aot == AddOnType.REMOTES:
                        value = value["co2"]

                self._attr_native_value = value

            self.async_write_ha_state()

        await mqtt.async_subscribe(
            self.hass, self.entity_description.key, message_received, 1
        )
