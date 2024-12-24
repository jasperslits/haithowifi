#!/usr/bin/env python3
"""Sensor component for Itho WiFi addon.

Author: Jasper
"""

import copy

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    _LOGGER,
    CONF_ADDON_TYPE,
    CONF_NONCVE_MODEL,
    MQTT_BASETOPIC,
    MQTT_STATETOPIC,
)
from .definitions.autotemp import (
    AUTOTEMP_COMM_SPACE_SENSOR_TEMPLATE,
    AUTOTEMP_DISTRIBUTOR_VALVE_SENSOR_TEMPLATE,
    AUTOTEMP_MALFUNCTION_VALVE_DECTECTION_DIST_SENSOR_TEMPLATE,
    AUTOTEMP_ROOM_SENSORS,
    AUTOTEMP_SENSORS,
    AUTOTEMP_VALVE_SENSOR_TEMPLATE,
)
from .definitions.co2_remote import REMOTE_SENSOR_TEMPLATE
from .definitions.cve import CVE_SENSORS
from .definitions.hru200 import HRU_ECO_200_SENSORS
from .definitions.hru250_300 import HRU_ECO_250_300_SENSORS
from .definitions.hru350 import HRU_ECO_350_SENSORS
from .definitions.hrueco import HRU_ECO_SENSORS
from .definitions.last_command import LAST_CMD_SENSORS
from .definitions.wpu import WPU_ERROR_CODE_BYTE_TEMPLATE, WPU_SENSORS
from .sensor_autotemp import IthoSensorAutotemp, IthoSensorAutotempRoom
from .sensor_co2_remote import IthoSensorCO2Remote
from .sensor_fan import IthoSensorFan
from .sensor_last_command import IthoSensorLastCommand
from .sensor_wpu import IthoSensorWPU


def _create_remotes(config_entry: ConfigEntry):
    """Create remotes for CO2 monitoring."""

    remotes = []
    for x in range(1, 5):
        remote = config_entry.data["remote" + str(x)]
        if remote not in ("", "Remote " + str(x)):
            sensor = copy.deepcopy(REMOTE_SENSOR_TEMPLATE)
            sensor.json_field = remote
            sensor.topic = f"{MQTT_BASETOPIC[config_entry.data[CONF_ADDON_TYPE]]}/{MQTT_STATETOPIC["remote"]}"
            sensor.translation_placeholders = {"remote_name": remote}
            sensor.unique_id = remote
            remotes.append(sensor)
    return remotes


def _create_autotemprooms(config_entry: ConfigEntry):
    """Create autotemp rooms for configured entries."""

    room_sensors = []
    for x in range(1, 8):
        template_sensors = copy.deepcopy(list(AUTOTEMP_ROOM_SENSORS))
        room = config_entry.data["room" + str(x)]
        if room not in ("", "Room " + str(x)):
            for sensor in template_sensors:
                sensor.json_field = sensor.json_field.replace("X", str(x))
                sensor.topic = (
                    f"{MQTT_BASETOPIC["autotemp"]}/{MQTT_STATETOPIC["autotemp"]}"
                )
                sensor.room = room
                sensor.unique_id = f"{sensor.translation_key}_{room}"
                room_sensors.append(sensor)

    return room_sensors


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
    if config_entry.data[CONF_ADDON_TYPE] == "autotemp":
        topic = f"{MQTT_BASETOPIC["autotemp"]}/{MQTT_STATETOPIC["autotemp"]}"
        for letter in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]:
            sensor = copy.deepcopy(AUTOTEMP_COMM_SPACE_SENSOR_TEMPLATE)
            sensor.topic = topic
            sensor.json_field = sensor.json_field.replace("X", letter)
            sensor.translation_placeholders = {"letter": letter}
            sensor.unique_id = sensor.unique_id_template.replace("x", letter)
            sensors.append(IthoSensorAutotemp(sensor, config_entry))

        for d in range(1, 4):
            for v in range(1, 13):
                d = str(d)
                v = str(v)
                sensor = copy.deepcopy(AUTOTEMP_DISTRIBUTOR_VALVE_SENSOR_TEMPLATE)
                sensor.topic = topic
                sensor.json_field = sensor.json_field.replace("X", d).replace("Y", v)
                sensor.translation_placeholders = {"distributor": d, "valve": v}
                sensor.unique_id = sensor.unique_id_template.replace("x", d).replace(
                    "y", v
                )
                sensors.append(IthoSensorAutotemp(sensor, config_entry))

        for d in range(1, 4):
            d = str(d)
            sensor = copy.deepcopy(
                AUTOTEMP_MALFUNCTION_VALVE_DECTECTION_DIST_SENSOR_TEMPLATE
            )
            sensor.topic = topic
            sensor.json_field = sensor.json_field.replace("X", d)
            sensor.translation_placeholders = {"distributor": d}
            sensor.unique_id = sensor.unique_id_template.replace("x", d)
            sensors.append(IthoSensorAutotemp(sensor, config_entry))

        for v in range(1, 4):
            v = str(v)
            template_sensors = copy.deepcopy(list(AUTOTEMP_VALVE_SENSOR_TEMPLATE))
            for sensor in template_sensors:
                sensor.topic = topic
                sensor.json_field = sensor.json_field.replace("X", v)
                sensor.translation_placeholders = {"valve": v}
                sensor.unique_id = sensor.unique_id_template.replace("x", v)
                sensors.append(IthoSensorAutotemp(sensor, config_entry))

        for description in AUTOTEMP_SENSORS:
            description.topic = (
                f"{MQTT_BASETOPIC["autotemp"]}/{MQTT_STATETOPIC["autotemp"]}"
            )
            sensors.append(IthoSensorAutotemp(description, config_entry))

        sensors.extend(
            [
                IthoSensorAutotempRoom(description, config_entry)
                for description in _create_autotemprooms(config_entry)
            ]
        )

    if config_entry.data[CONF_ADDON_TYPE] == "cve":
        topic = f"{MQTT_BASETOPIC["cve"]}/{MQTT_STATETOPIC["cve"]}"

        for description in CVE_SENSORS:
            description.topic = topic
            sensors.append(IthoSensorFan(description, config_entry))

    if config_entry.data[CONF_ADDON_TYPE] == "noncve":
        topic = f"{MQTT_BASETOPIC["noncve"]}/{MQTT_STATETOPIC["noncve"]}"

        if config_entry.data[CONF_NONCVE_MODEL] == "hru_eco":
            hru_sensors = HRU_ECO_SENSORS
        if config_entry.data[CONF_NONCVE_MODEL] == "hru_eco_200":
            hru_sensors = HRU_ECO_200_SENSORS
        if config_entry.data[CONF_NONCVE_MODEL] in ["hru_eco_250", "hru_eco_300"]:
            hru_sensors = HRU_ECO_250_300_SENSORS
        if config_entry.data[CONF_NONCVE_MODEL] == "hru_eco_350":
            hru_sensors = HRU_ECO_350_SENSORS

        for description in hru_sensors:
            description.topic = topic
            sensors.append(IthoSensorFan(description, config_entry))

    if config_entry.data[CONF_ADDON_TYPE] in ["cve", "noncve"]:
        topic = f"{MQTT_BASETOPIC[config_entry.data[CONF_ADDON_TYPE]]}/{MQTT_STATETOPIC["last_cmd"]}"

        sensors.extend(
            [
                IthoSensorCO2Remote(description, config_entry)
                for description in _create_remotes(config_entry)
            ]
        )

        for description in LAST_CMD_SENSORS:
            description.topic = topic
            sensors.append(IthoSensorLastCommand(description, config_entry))

    if config_entry.data[CONF_ADDON_TYPE] == "wpu":
        topic = f"{MQTT_BASETOPIC["wpu"]}/{MQTT_STATETOPIC["wpu"]}"
        for x in range(6):
            x = str(x)
            sensor = copy.deepcopy(WPU_ERROR_CODE_BYTE_TEMPLATE)
            sensor.topic = topic
            sensor.json_field = sensor.json_field + x
            sensor.translation_placeholders = {"num": x}
            sensor.unique_id = sensor.unique_id_template.replace("x", x)
            sensors.append(IthoSensorWPU(sensor, config_entry))

        for description in WPU_SENSORS:
            description.topic = topic
            sensors.append(IthoSensorWPU(description, config_entry))

    async_add_entities(sensors)
