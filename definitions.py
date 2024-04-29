"""Definitions for Itho sensors added to MQTT."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Final

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfTemperature,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfPressure,
    REVOLUTIONS_PER_MINUTE,
    PERCENTAGE
)
from homeassistant.util import dt as dt_util

from .const.const import CONF_HRU_STATETOPIC,CONF_WPU_STATETOPIC,CONF_AUTOTEMP_STATETOPIC

@dataclass(frozen=True)
class IthoSensorEntityDescription(SensorEntityDescription):
    """Sensor entity description for Itho."""

    state: Callable | None = None
    json_field : str | None = None


WPUSENSORS: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field = "CV pressure (Bar)",
        key=CONF_WPU_STATETOPIC,
        translation_key="cv_pressure",
        device_class=SensorDeviceClass.PRESSURE,
        native_unit_of_measurement=UnitOfPressure.BAR,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field = "Flow sensor (lt_hr)",
        key=CONF_WPU_STATETOPIC,
        translation_key="flow_sensor",
        state_class=SensorStateClass.MEASUREMENT,
    ),
     IthoSensorEntityDescription(
        json_field = "Heat demand thermost. (%)",
        key=CONF_WPU_STATETOPIC,
        translation_key="heat_demand",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field = "CV return temp (°C)",
        key=CONF_WPU_STATETOPIC,
        translation_key="cv_return_temp",
         device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field = "Boiler temp up (°C)",
        key=CONF_WPU_STATETOPIC,
        translation_key="boiler_temp_up",
     device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
     IthoSensorEntityDescription(
        json_field = "Status",
        key=CONF_WPU_STATETOPIC,
        translation_key="status"
    ),
    IthoSensorEntityDescription(
        json_field = "Room temp (°C)",
        key=CONF_WPU_STATETOPIC,
        translation_key="room_temp",
     device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field = "Cv pump (%)",
        key=CONF_WPU_STATETOPIC,
        translation_key="cv_pump_percent",
      native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field = "Well pump (%)",
        key=CONF_WPU_STATETOPIC,
        translation_key="well_pump_percent",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field = "Boiler pump (%)",
        key=CONF_WPU_STATETOPIC,
        translation_key="boiler_pump_percent",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
       IthoSensorEntityDescription(
        json_field = "Temp to source (°C)",
        key=CONF_WPU_STATETOPIC,
        translation_key="temp_to_source",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field = "Temp from source (°C)",
        key=CONF_WPU_STATETOPIC,
        translation_key="temp_from_source",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
     IthoSensorEntityDescription(
        json_field = "Requested room temp (°C)",
        key=CONF_WPU_STATETOPIC,
        translation_key="requested_room_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # Requested room temp (°C)
   # // Boiler temp up (°C)
)

AUTOTEMPSENSORS: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field = "Room X power % (%)",
        key=CONF_AUTOTEMP_STATETOPIC,
        translation_key="room_x_power_percent",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field = "Room X actual temp",
        key=CONF_AUTOTEMP_STATETOPIC,
        translation_key="room_x_actual_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field = "Room X power kW",
        key=CONF_AUTOTEMP_STATETOPIC,
        translation_key="actual_x_",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field = "Room X power % (%)",
        key=CONF_AUTOTEMP_STATETOPIC,
        translation_key="actual_supply_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),

    )

"""
- name: Itho slaapkamer evi power percent
  state_topic: "ithotemp/ithostatus"
  value_template: "{{ value_json['Room 3 power % (%)'] }}"
  unique_id: "itho_slaapkamerevi_power_percentage"
  state_class: "measurement"
  device_class: "power_factor"
  unit_of_measurement: "%"

- name: Itho slaapkamer evi temp actual
  state_topic: "ithotemp/ithostatus"
  value_template: "{{ value_json['Room 3 temp'] }}"
  unique_id: "itho_slaapkamerevi_temp_actual"
  state_class: "measurement"
  device_class: "temperature"
  unit_of_measurement: "°C"

- name: Itho slaapkamer evi temp target
  state_topic: "ithotemp/ithostatus"
  value_template: "{{ value_json['Room 3 setp'] }}"
  unique_id: "itho_slaapkamerevi_temp_target"
  state_class: "measurement"
  device_class: "temperature"
  unit_of_measurement: "°C"

- name: Itho slaapkamer evi power kw
  state_topic: "ithotemp/ithostatus"
  value_template: "{{ value_json['Room 3 power kW (kW)'] }}"
  unique_id: "itho_slaapkamerevi_powerkw"
  state_class: "measurement"
  device_class: "power"
  unit_of_measurement: "kW"
"""

HRUSENSORS: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field = "Supply temp (°C)",
        key=CONF_HRU_STATETOPIC,
        translation_key="actual_supply_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
	IthoSensorEntityDescription(
        json_field = "Exhaust temp (°C)",
        key=CONF_HRU_STATETOPIC,
        translation_key="actual_exhaust_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field = "Supply fan (RPM)",
        key=CONF_HRU_STATETOPIC,
        translation_key="actual_supply_fan",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field = "Exhaust fan (RPM)",
        key=CONF_HRU_STATETOPIC,
        translation_key="actual_exhaust_fan",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field = "Balance (%)",
        key=CONF_HRU_STATETOPIC,
        translation_key="balance",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field = "Air Quality (%)",
        key=CONF_HRU_STATETOPIC,
        translation_key="airquality",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
     IthoSensorEntityDescription(
        json_field = "Actual Mode",
        key=CONF_HRU_STATETOPIC,
        translation_key="actual_mode"
    ),
    
    
)
