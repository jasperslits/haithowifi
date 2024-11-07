#!/usr/bin/env python3
"""Sensor component for Itho WiFi addon.

Author: Jasper
"""

import copy
import json
from datetime import datetime, timedelta

from homeassistant.components import mqtt
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    _LOGGER,
    ADDONS,
    CONF_CVE_TYPE,
    CONF_USE_AUTOTEMP,
    CONF_USE_REMOTES,
    CONF_USE_WPU,
    HRU_ACTUAL_MODE,
    HRU_GLOBAL_FAULT_CODE,
    MQTT_BASETOPIC,
    MQTT_STATETOPIC,
    RH_ERROR_CODE,
    UNITTYPE_ICONS,
    WPU_STATUS,
    AddOnType,
)
from .definitions import (
    AUTOTEMPSENSORS,
    CVESENSORS,
    NONCVESENSORS,
    WPUSENSORS,
    IthoSensorEntityDescription,
)


def _create_remotes(config_entry: ConfigEntry):
    """Create remotes for CO2 monitoring."""

    cfg = config_entry.data
    REMOTES = []
    for x in range(1, 5):
        remote = cfg["remote" + str(x)]
        if remote != "" and remote != "Remote " + str(x):
            REMOTES.append(IthoSensorEntityDescription(
                json_field=remote,
                key=f"{MQTT_BASETOPIC[config_entry.data[CONF_CVE_TYPE]]}/{MQTT_STATETOPIC["remotes"]}",
                translation_key=remote,
                device_class="carbon_dioxide",
                native_unit_of_measurement="ppm",
                state_class="measurement"))
    return REMOTES


def _create_autotemprooms(config_entry: ConfigEntry):
    """Create autotemp rooms for configured entries."""

    cfg = config_entry.data
    configured_sensors = []
    for x in range(1, 8):
        template_sensors = copy.deepcopy(list(AUTOTEMPSENSORS))
        room = cfg["room" + str(x)]
        if room != "" and room != "Room " + str(x):

            for sensor in template_sensors:
                sensor.key = f"{MQTT_BASETOPIC["autotemp"]}/{MQTT_STATETOPIC["autotemp"]}"
                sensor.json_field = sensor.json_field.replace("X", str(x))
                sensor.translation_key = sensor.translation_key.replace("Room X", room)
                configured_sensors.append(sensor)

    return configured_sensors


async def async_setup_entry(
    _: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Itho add-on sensors from config entry based on their type."""
    if config_entry.data[CONF_CVE_TYPE] == "noncve":
        for description in NONCVESENSORS:
            description.key = f"{MQTT_BASETOPIC["noncve"]}/{MQTT_STATETOPIC["noncve"]}"
            async_add_entities(IthoSensor(description, config_entry, AddOnType.NONCVE))

    if config_entry.data[CONF_CVE_TYPE] == "cve":
        for description in CVESENSORS:
            description.key = f"{MQTT_BASETOPIC["cve"]}/{MQTT_STATETOPIC["cve"]}"
            async_add_entities(IthoSensor(description, config_entry, AddOnType.CVE))

    if config_entry.data[CONF_USE_WPU]:
        for description in WPUSENSORS:
            description.key = f"{MQTT_BASETOPIC["wpu"]}/{MQTT_STATETOPIC["wpu"]}"
            async_add_entities(IthoSensor(description, config_entry, AddOnType.WPU) for description in WPUSENSORS)

    if config_entry.data[CONF_USE_REMOTES]:
        async_add_entities(IthoSensor(description, config_entry, AddOnType.REMOTES) for description in _create_remotes(config_entry))

    if config_entry.data[CONF_USE_AUTOTEMP]:
        async_add_entities(IthoSensor(description, config_entry, AddOnType.AUTOTEMP) for description in _create_autotemprooms(config_entry))


class IthoSensor(SensorEntity):
    """Representation of a Itho add-on sensor that is updated via MQTT."""

    _attr_has_entity_name = True
    entity_description: IthoSensorEntityDescription

    _filter_last_maintenance = None
    _filter_next_maintenance_estimate = None
    _global_fault_code_description = None
    _rh_error_description = None

    def __init__(
        self, description: IthoSensorEntityDescription, config_entry: ConfigEntry, aot: AddOnType
    ) -> None:
        """Initialize the sensor."""
        self.entity_description = description

        self.entity_id = f"sensor.{ADDONS[aot].lower()}_{description.translation_key}"
        self._attr_unique_id = f"{config_entry.entry_id}-{description.translation_key}"
        self.aot = aot

    @property
    def name(self) -> str:
        """Generate name for the sensor."""
        return self.entity_description.translation_key.replace("_", " ").capitalize()

    @property
    def icon(self) -> str|None:
        """Pick the right icon."""

        if self.entity_description.icon is not None:
            return self.entity_description.icon
        if self.entity_description.native_unit_of_measurement in UNITTYPE_ICONS:
            return UNITTYPE_ICONS[self.entity_description.native_unit_of_measurement]
        return None

    @property
    def extra_state_attributes(self) -> list[str]|None:
        """Return the state attributes."""

        if self._global_fault_code_description is not None:
            return {
                "Description": self._global_fault_code_description,
            }

        if self._filter_last_maintenance is not None and self._filter_next_maintenance_estimate is not None:
            return {
                "Last Maintenance": self._filter_last_maintenance,
                "Next Maintenance Estimate": self._filter_next_maintenance_estimate,
            }

        if self._rh_error_description is not None:
            return {
                "Error Description": self._rh_error_description,
            }
        return None

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
                    if self.aot == AddOnType.NONCVE:
                        if self.entity_description.json_field == "Actual Mode":
                            value = HRU_ACTUAL_MODE[value]

                        if self.entity_description.json_field == "Airfilter counter":
                            try:
                                self._filter_last_maintenance = (datetime.now() - timedelta(hours=int(value))).date()
                                self._filter_next_maintenance_estimate = (datetime.now() + timedelta(days=180, hours=-int(value))).date()
                            except ValueError as e:
                                _LOGGER.error(f"failed to parse value for 'Airfilter counter'\n{e}")

                        if self.entity_description.json_field == "Global fault code":
                            self._global_fault_code_description = HRU_GLOBAL_FAULT_CODE.get(int(value), "Unknown fault code")

                    if self.aot == AddOnType.WPU and self.entity_description.json_field == "Status":
                        value = WPU_STATUS[value]

                    if self.aot == AddOnType.REMOTES:
                        value = value["co2"]

                if self.entity_description.json_field == "Highest received RH value (%RH)":
                    if value.isnumeric() and float(value) > 100:
                        self._attr_native_value = None
                        self._rh_error_description = RH_ERROR_CODE.get(int(value), "Unknown Error")
                    else:
                        self._attr_native_value = value
                        self._rh_error_description = ""
                else:
                    self._attr_native_value = value

            self.async_write_ha_state()

        await mqtt.async_subscribe(
            self.hass, self.entity_description.key, message_received, 1
        )
