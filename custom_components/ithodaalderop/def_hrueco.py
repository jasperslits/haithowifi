"""Definitions for Itho sensors added to MQTT."""

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    PERCENTAGE,
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
    IthoBinarySensorEntityDescription(
        json_field="Valve position (pulse)",
        translation_key="valve_position",
        device_class=BinarySensorDeviceClass.OPENING,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon_off="mdi:valve-closed",
        icon_on="mdi:valve-open",
        entity_registry_enabled_default=False,
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
        json_field="Balance (%)",
        translation_key="balance",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="boiler timer (min)",
        translation_key="boiler_timer",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Current pos",
        translation_key="current_pos",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Drain actual (rpm)",
        translation_key="drain_actual",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Drain fan speed (rpm)",
        translation_key="drain_fan_speed",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Drain requested (rpm)",
        translation_key="drain_requested",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Frost lock",
        translation_key="frost_lock",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Frost timer (sec)",
        translation_key="frost_timer",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="GHE switch",
        translation_key="ghe_switch",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Outdoor temp (°C)",
        translation_key="outdoor_temp",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Temp of exhaust air (°C)",
        translation_key="actual_exhaust_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Requested speed (%)",
        translation_key="requested_speed",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
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
        json_field="summer counter",
        translation_key="summer_counter",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Summer day",
        translation_key="summer_day",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Supply actual (rpm)",
        translation_key="supply_actual",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Supply fan speed (rpm)",
        translation_key="supply_fan_speed",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Supply requested (rpm)",
        translation_key="supply_requested",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Temp of supply air (°C)",
        translation_key="actual_supply_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="VKK switch",
        translation_key="vkk_switch",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
)
