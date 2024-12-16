"""Definitions for Itho sensors added to MQTT."""

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
    REVOLUTIONS_PER_MINUTE,
    EntityCategory,
    UnitOfTemperature,
    UnitOfTime,
)

from .definitions import IthoBinarySensorEntityDescription, IthoSensorEntityDescription

HRUECO200SENSORS: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field="Actual speed (rpm)",
        translation_key="actual_speed",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Air discharge temperature (°C)",
        translation_key="air_discharge_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Average air outlet temperature (°C)",
        translation_key="average_air_outlet_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Error",
        translation_key="error",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    IthoSensorEntityDescription(
        json_field="Filter use counter (hour)",
        translation_key="filter_use_counter",
        native_unit_of_measurement=UnitOfTime.HOURS,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:counter",
    ),
    IthoSensorEntityDescription(
        json_field="Max. CO2 level (ppm)",
        translation_key="max_co2_level",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        icon="mdi:molecule-co2",
    ),
    IthoSensorEntityDescription(
        json_field="Max. RH level (%)",
        translation_key="max_rh_level",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Room temp setpoint (°C)",
        translation_key="room_temp_setpoint",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Outside temperature (°C)",
        translation_key="outside_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Speed setpoint (rpm)",
        translation_key="speed_setpoint",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Total operation (hrs)",
        translation_key="total_operation_time",
        native_unit_of_measurement=UnitOfTime.HOURS,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    IthoSensorEntityDescription(
        json_field="Ventilation setpoint (%)",
        translation_key="ventilation_setpoint_percentage",
        native_unit_of_measurement=PERCENTAGE,
    ),
)
