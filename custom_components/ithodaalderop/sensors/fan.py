"""Sensor class for handling Fan sensors."""

from datetime import datetime, timedelta
import json

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ..const import (
    CONF_NONCVE_MODEL,
    HRU_ECO_250_300_ERROR_CODE,
    HRU_ECO_350_ACTUAL_MODE,
    HRU_ECO_350_GLOBAL_FAULT_CODE,
    HRU_ECO_350_RH_ERROR_CODE,
    HRU_ECO_STATUS,
)
from ..definitions.cve import CVE_BINARY_SENSORS, CVE_SENSORS
from ..definitions.demandflow import DEMAND_FLOW_BINARY_SENSORS, DEMAND_FLOW_SENSORS
from ..definitions.hru200 import HRU_ECO_200_SENSORS
from ..definitions.hru250_300 import HRU_ECO_250_300_SENSORS
from ..definitions.hru350 import HRU_ECO_350_BINARY_SENSORS, HRU_ECO_350_SENSORS
from ..definitions.hrueco import HRU_ECO_BINARY_SENSORS, HRU_ECO_SENSORS
from ..utils import get_mqtt_state_topic
from .base_sensors import IthoBaseSensor, IthoBinarySensor


def get_cve_binary_sensors(config_entry: ConfigEntry):
    """Create binary sensors for CVE."""
    sensors = []
    for description in CVE_BINARY_SENSORS:
        description.topic = f"{get_mqtt_state_topic(config_entry.data)}"
        sensors.append(IthoBinarySensor(description, config_entry))

    return sensors


def get_cve_sensors(config_entry: ConfigEntry):
    """Create sensors for CVE."""
    sensors = []

    for description in CVE_SENSORS:
        description.topic = f"{get_mqtt_state_topic(config_entry.data)}"
        sensors.append(IthoSensorFan(description, config_entry))

    return sensors


def get_noncve_binary_sensors(config_entry: ConfigEntry):
    """Create binary sensors for NON-CVE."""
    sensors = []

    if config_entry.data[CONF_NONCVE_MODEL] in ["hru_eco", "hru_eco_350"]:
        if config_entry.data[CONF_NONCVE_MODEL] == "hru_eco":
            hru_sensors = HRU_ECO_BINARY_SENSORS
        if config_entry.data[CONF_NONCVE_MODEL] == "hru_eco_350":
            hru_sensors = HRU_ECO_350_BINARY_SENSORS
        if config_entry.data[CONF_NONCVE_MODEL] == "demand_flow":
            hru_sensors = DEMAND_FLOW_BINARY_SENSORS

        for description in hru_sensors:
            description.topic = f"{get_mqtt_state_topic(config_entry.data)}"
            sensors.append(IthoBinarySensor(description, config_entry))

    return sensors


def get_noncve_sensors(config_entry: ConfigEntry):
    """Create sensors for NON-CVE."""
    sensors = []

    if config_entry.data[CONF_NONCVE_MODEL] == "hru_eco":
        hru_sensors = HRU_ECO_SENSORS
    if config_entry.data[CONF_NONCVE_MODEL] == "hru_eco_200":
        hru_sensors = HRU_ECO_200_SENSORS
    if config_entry.data[CONF_NONCVE_MODEL] in ["hru_eco_250", "hru_eco_300"]:
        hru_sensors = HRU_ECO_250_300_SENSORS
    if config_entry.data[CONF_NONCVE_MODEL] == "hru_eco_350":
        hru_sensors = HRU_ECO_350_SENSORS
    if config_entry.data[CONF_NONCVE_MODEL] == "demand_flow":
        hru_sensors = DEMAND_FLOW_SENSORS

    for description in hru_sensors:
        description.topic = f"{get_mqtt_state_topic(config_entry.data)}"
        sensors.append(IthoSensorFan(description, config_entry))

    return sensors


class IthoSensorFan(IthoBaseSensor):
    """Representation of a Itho add-on sensor that is updated via MQTT."""

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
            value = payload[json_field]
            # HRU ECO 350
            if json_field == "Actual Mode":
                self._extra_state_attributes = {"Code": value}
                value = HRU_ECO_350_ACTUAL_MODE.get(value, "Unknown mode")

            # HRU ECO 350
            if json_field == "Air Quality (%)":
                _error_description = "Unknown error code"
                if isinstance(value, (int, float)) and float(value) > 100:
                    _error_description = "Unknown error"
                    value = None

                self._extra_state_attributes = {
                    "Error Description": _error_description,
                }

            # HRU ECO 350 / HRU ECO
            if json_field in ["Airfilter counter", "Air filter counter"]:
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

            # HRU ECO 250/300
            if json_field == "Error number":
                _description = ""
                if str(value).isnumeric():
                    _error_description = HRU_ECO_250_300_ERROR_CODE.get(
                        int(value), _description
                    )

                self._extra_state_attributes = {
                    "Description": _description,
                }

            # HRU ECO 350
            if json_field == "Global fault code":
                _description = "Unknown fault code"
                if str(value).isnumeric():
                    _description = HRU_ECO_350_GLOBAL_FAULT_CODE.get(
                        int(value), _description
                    )

                self._extra_state_attributes = {
                    "Description": _description,
                }

            # HRU ECO 350
            if json_field == "Highest received RH value (%RH)":
                _error_description = ""
                if isinstance(value, (int, float)) and float(value) > 100:
                    _error_description = HRU_ECO_350_RH_ERROR_CODE.get(
                        int(value), "Unknown error"
                    )
                    value = None

                self._extra_state_attributes = {
                    "Error Description": _error_description,
                }

            # HRU ECO
            if json_field == "Status":
                self._extra_state_attributes = {
                    "Code": value,
                }

                _description = "Unknown status"
                if str(value).isnumeric():
                    _description = HRU_ECO_STATUS.get(int(value), _description)
                value = _description

        self._attr_native_value = value
        self.async_write_ha_state()
