"""Definitions for Itho sensors added to MQTT."""

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    REVOLUTIONS_PER_MINUTE,
    EntityCategory,
    UnitOfTemperature,
    UnitOfTime,
)

from .definitions import IthoBinarySensorEntityDescription, IthoSensorEntityDescription

HRUECOBINARYSENSORS: tuple[IthoBinarySensorEntityDescription, ...] = (
    IthoBinarySensorEntityDescription(
        json_field="Bypass position (pulse)",
        translation_key="bypass_position",
        device_class=BinarySensorDeviceClass.OPENING,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon_off="mdi:valve-closed",
        icon_on="mdi:valve-open",
    ),
)

HRUECOSENSORS: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field="Air filter counter",
        translation_key="airfilter_counter",
        native_unit_of_measurement=UnitOfTime.HOURS,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:counter",
    ),
    IthoSensorEntityDescription(
        json_field="Drain fan speed (rpm)",
        translation_key="drain_fan_speed",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Temp of exhaust air (°C)",
        translation_key="actual_exhaust_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="room temp (°C)",
        translation_key="room_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Status",
        translation_key="status",
    ),
    IthoSensorEntityDescription(
        json_field="Supply fan speed (rpm)",
        translation_key="supply_fan_speed",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Temp of supply air (°C)",
        translation_key="actual_supply_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)
