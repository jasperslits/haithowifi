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

CVEBINARYSENSORS: tuple[IthoBinarySensorEntityDescription, ...] = (
    IthoBinarySensorEntityDescription(
        json_field="Filter dirty",
        translation_key="filter_dirty",
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon_off="mdi:air-filter",
        icon_on="mdi:vacuum-outline",
    ),
)

CVESENSORS: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field="Error",
        translation_key="error",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    IthoSensorEntityDescription(
        json_field="Fan setpoint (rpm)",
        translation_key="fan_setpoint_rpm",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Fan speed (rpm)",
        translation_key="fan_speed",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Highest CO2 concentration (ppm)",
        translation_key="highest_received_co2_value",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        icon="mdi:molecule-co2",
    ),
    IthoSensorEntityDescription(
        json_field="Highest RH concentration (%)",
        translation_key="highest_received_rh_value",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="hum",
        translation_key="humidity",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="temp",
        translation_key="temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Total operation (hours)",
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
