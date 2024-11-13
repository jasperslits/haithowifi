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
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    _LOGGER,
    ADDON_TYPES,
    ADDONS,
    AUTOTEMP_ERROR,
    AUTOTEMP_MODE,
    CONF_ADDON_TYPE,
    DOMAIN,
    MQTT_BASETOPIC,
    MQTT_STATETOPIC,
    NONCVE_ACTUAL_MODE,
    NONCVE_GLOBAL_FAULT_CODE,
    NONCVE_RH_ERROR_CODE,
    UNITTYPE_ICONS,
    WPU_STATUS,
    AddOnType,
)
from .definitions import (
    AUTOTEMPROOMSENSORS,
    AUTOTEMPSENSORS,
    CVESENSORS,
    NONCVESENSORS,
    WPUSENSORS,
    IthoSensorEntityDescription,
)


def _create_remotes(config_entry: ConfigEntry):
    """Create remotes for CO2 monitoring."""

    cfg = config_entry.data
    remotes = []
    for x in range(1, 5):
        remote = cfg["remote" + str(x)]
        if remote != "" and remote != "Remote " + str(x):
            remotes.append(
                IthoSensorEntityDescription(
                    json_field=remote,
                    key=f"{MQTT_BASETOPIC[config_entry.data[CONF_ADDON_TYPE]]}/{MQTT_STATETOPIC["remote"]}",
                    translation_key=remote,
                    device_class="carbon_dioxide",
                    native_unit_of_measurement="ppm",
                    state_class="measurement",
                )
            )
    return remotes


def _create_autotemprooms(config_entry: ConfigEntry):
    """Create autotemp rooms for configured entries."""

    cfg = config_entry.data
    configured_sensors = []
    for x in range(1, 8):
        template_sensors = copy.deepcopy(list(AUTOTEMPROOMSENSORS))
        room = cfg["room" + str(x)]
        if room != "" and room != "Room " + str(x):
            for sensor in template_sensors:
                sensor.key = (
                    f"{MQTT_BASETOPIC["autotemp"]}/{MQTT_STATETOPIC["autotemp"]}"
                )
                sensor.json_field = sensor.json_field.replace("X", str(x))
                sensor.translation_key = sensor.translation_key.replace("Room X", room)
                configured_sensors.append(sensor)

    return configured_sensors


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Itho add-on sensors from config entry based on their type."""

    if not await mqtt.async_wait_for_mqtt_client(hass):
        _LOGGER.error("MQTT integration is not available")
        return

    sensors = []
    if config_entry.data[CONF_ADDON_TYPE] == "noncve":
        for description in NONCVESENSORS:
            description.key = f"{MQTT_BASETOPIC["noncve"]}/{MQTT_STATETOPIC["noncve"]}"
            sensors.append(IthoSensorFan(description, config_entry, AddOnType.NONCVE))

    if config_entry.data[CONF_ADDON_TYPE] == "cve":
        for description in CVESENSORS:
            description.key = f"{MQTT_BASETOPIC["cve"]}/{MQTT_STATETOPIC["cve"]}"
            sensors.append(IthoSensorFan(description, config_entry, AddOnType.CVE))

    if config_entry.data[CONF_ADDON_TYPE] in ["cve", "noncve"]:
        for description in _create_remotes(config_entry):
            description.key = f"{MQTT_BASETOPIC[config_entry.data[CONF_ADDON_TYPE]]}/{MQTT_STATETOPIC["remote"]}"
            sensors.append(IthoSensorRemote(description, config_entry))

    if config_entry.data[CONF_ADDON_TYPE] == "wpu":
        for description in WPUSENSORS:
            description.key = f"{MQTT_BASETOPIC["wpu"]}/{MQTT_STATETOPIC["wpu"]}"
            sensors.append(IthoSensorWPU(description, config_entry))

    if config_entry.data[CONF_ADDON_TYPE] == "autotemp":
        for description in list(AUTOTEMPSENSORS) + _create_autotemprooms(config_entry):
            description.key = (
                f"{MQTT_BASETOPIC["autotemp"]}/{MQTT_STATETOPIC["autotemp"]}"
            )
            sensors.append(IthoSensorAutotemp(description, config_entry))

    async_add_entities(sensors)


class IthoBaseSensor(SensorEntity):
    """Base class sharing foundation for WPU, remotes and Fans."""

    _attr_has_entity_name = True
    entity_description: IthoSensorEntityDescription

    _extra_state_attributes = None

    def __init__(
        self,
        description: IthoSensorEntityDescription,
        config_entry: ConfigEntry,
        aot: AddOnType,
    ) -> None:
        """Initialize the sensor."""
        self.entity_description = description

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.data[CONF_ADDON_TYPE])},
            manufacturer="Arjen Hiemstra",
            model="CVE" if aot == AddOnType.CVE else "NONCVE",
            name="Itho " + ADDON_TYPES[config_entry.data[CONF_ADDON_TYPE]],
        )

        self.entity_id = f"sensor.{ADDONS[aot].lower()}_{description.translation_key}"
        self._attr_unique_id = f"{config_entry.entry_id}-{description.translation_key}"
        self.aot = aot

    @property
    def icon(self) -> str | None:
        """Pick the right icon."""

        if self.entity_description.icon is not None:
            return self.entity_description.icon
        if self.entity_description.native_unit_of_measurement in UNITTYPE_ICONS:
            return UNITTYPE_ICONS[self.entity_description.native_unit_of_measurement]
        return None


class IthoSensorRemote(IthoBaseSensor):
    """Representation of Itho add-on sensor for a Remote that is updated via MQTT."""

    def __init__(
        self, description: IthoSensorEntityDescription, config_entry: ConfigEntry
    ) -> None:
        """Construct sensor for Remote."""
        super().__init__(description, config_entry, AddOnType.REMOTE)

    @property
    def name(self) -> str:
        """Generate name for the sensor."""
        return self.entity_description.translation_key.replace("_", " ").capitalize()

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""

        @callback
        def message_received(message):
            """Handle new MQTT messages."""
            if message.payload == "":
                value = None
            elif self.entity_description.state is not None:
                value = self.entity_description.state(message.payload)
            else:
                payload = json.loads(message.payload)
                if self.entity_description.json_field not in payload:
                    value = None
                else:
                    value = payload[self.entity_description.json_field]["co2"]

            self._attr_native_value = value
            self.async_write_ha_state()

        await mqtt.async_subscribe(
            self.hass, self.entity_description.key, message_received, 1
        )


class IthoSensorAutotemp(IthoBaseSensor):
    """Representation of Itho add-on sensor for Autotemp data that is updated via MQTT."""

    def __init__(
        self, description: IthoSensorEntityDescription, config_entry: ConfigEntry
    ) -> None:
        """Construct sensor for Autotemp."""
        super().__init__(description, config_entry, AddOnType.AUTOTEMP)

    @property
    def name(self) -> str:
        """Generate name for the sensor."""
        return self.entity_description.translation_key.replace("_", " ").capitalize()

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""

        @callback
        def message_received(message):
            """Handle new MQTT messages."""
            if message.payload == "":
                value = None
            elif self.entity_description.state is not None:
                value = self.entity_description.state(message.payload)
            else:
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


class IthoSensorWPU(IthoBaseSensor):
    """Representation of Itho add-on sensor for WPU that is updated via MQTT."""

    def __init__(
        self, description: IthoSensorEntityDescription, config_entry: ConfigEntry
    ) -> None:
        """Construct sensor for WPU."""
        super().__init__(description, config_entry, AddOnType.WPU)

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""

        @callback
        def message_received(message):
            """Handle new MQTT messages."""
            if message.payload == "":
                value = None
            elif self.entity_description.state is not None:
                value = self.entity_description.state(message.payload)
            else:
                payload = json.loads(message.payload)
                json_field = self.entity_description.json_field
                if json_field not in payload:
                    value = None
                else:
                    value = payload[json_field]
                    if json_field == "Status":
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


class IthoSensorFan(IthoBaseSensor):
    """Representation of a Itho add-on sensor that is updated via MQTT."""

    _attr_has_entity_name = True
    entity_description: IthoSensorEntityDescription

    _extra_state_attributes = None

    def __init__(
        self,
        description: IthoSensorEntityDescription,
        config_entry: ConfigEntry,
        aot: AddOnType,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(description, config_entry, aot)

    @property
    def extra_state_attributes(self) -> list[str] | None:
        """Return the state attributes."""
        return self._extra_state_attributes

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""

        @callback
        def message_received(message):
            """Handle new MQTT messages."""
            if message.payload == "":
                value = None
            elif self.entity_description.state is not None:
                value = self.entity_description.state(message.payload)
            else:
                payload = json.loads(message.payload)
                if self.entity_description.json_field not in payload:
                    value = None
                else:
                    value = payload[self.entity_description.json_field]
                    json_field = self.entity_description.json_field

                    if json_field == "Actual Mode":
                        self._extra_state_attributes = {"Code": value}
                        value = NONCVE_ACTUAL_MODE.get(value, "Unknown mode")

                    if json_field == "Airfilter counter":
                        _last_maintenance = ""
                        _next_maintenance_estimate = ""
                        if str(value).isnumeric():
                            _last_maintenance = (
                                datetime.now() - timedelta(hours=int(value))
                            ).date()
                            _next_maintenance_estimate = (
                                datetime.now() + timedelta(days=180, hours=-int(value))
                            ).date()
                        else:
                            _last_maintenance = "Invalid value"

                        self._extra_state_attributes = {
                            "Last Maintenance": _last_maintenance,
                            "Next Maintenance Estimate": _next_maintenance_estimate,
                        }

                    if json_field == "Global fault code":
                        _description = ""
                        if str(value).isnumeric():
                            _description = NONCVE_GLOBAL_FAULT_CODE.get(
                                int(value), "Unknown fault code"
                            )

                        self._extra_state_attributes = {
                            "Description": _description,
                        }

                    if json_field == "Highest received RH value (%RH)":
                        _error_description = ""
                        if isinstance(value, int) and float(value) > 100:
                            _error_description = NONCVE_RH_ERROR_CODE.get(
                                int(value), "Unknown error"
                            )
                            value = None
                        else:
                            _error_description = ""

                        self._extra_state_attributes = {
                            "Error Description": _error_description,
                        }

            self._attr_native_value = value
            self.async_write_ha_state()

        await mqtt.async_subscribe(
            self.hass, self.entity_description.key, message_received, 1
        )
