"""Definitions for Itho HRU 200 sensors added to MQTT."""

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
    REVOLUTIONS_PER_MINUTE,
    EntityCategory,
    UnitOfTemperature,
    UnitOfTime,
)

from .base_definitions import IthoSensorEntityDescription

HRU_ECO_200_SENSORS: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field="Absence (min)",
        key="absence",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Actual speed (rpm)",
        key="actual_speed",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="Air discharge temperature (°C)",
        key="air_discharge_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="Average air outlet temperature (°C)",
        key="average_air_outlet_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="Block timer bypass (min)",
        key="block_timer_bypass",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Bypass mode",
        key="bypass_mode",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Bypass setpoint (%)",
        key="bypass_setpoint",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Current bypass share (%)",
        key="current_bypass_share",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Deferred absence (min)",
        key="deferred_absence",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Duration of current frost setpoint (sec)",
        key="duration_of_current_frost_setpoint",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Error",
        key="error",
        entity_category=EntityCategory.DIAGNOSTIC,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="Fan off during frost (min)",
        key="fan_off_during_frost",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Filter use counter (hour)",
        key="filter_use_counter",
        native_unit_of_measurement=UnitOfTime.HOURS,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:counter",
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="Frost adjustment speed (rpm)",
        key="frost_adjustment_speed",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Frost status",
        key="frost_status",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Max. CO2 level (ppm)",
        key="max_co2_level",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        icon="mdi:molecule-co2",
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="Max frost vent. speed (rpm)",
        key="max_frost_vent_speed",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Max. RH level (%)",
        key="max_rh_level",
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="Number of bypass settings",
        key="number_of_bypass_settings",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Periodic bypass valve travel (min)",
        key="periodic_bypass_valve_travel",
        native_unit_of_measurement=UnitOfTime.MINUTES,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Position of frost valve (%)",
        key="position_of_frost_valve",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Room temp setpoint (°C)",
        key="room_temp_setpoint",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="Outside temperature (°C)",
        key="outside_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="Selection",
        key="selection",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Speed setpoint (rpm)",
        key="speed_setpoint",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="Start-up counter",
        key="start_up_counter",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Total operation (hrs)",
        key="total_operation_time",
        native_unit_of_measurement=UnitOfTime.HOURS,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="Ventilation setpoint (%)",
        key="ventilation_setpoint_percentage",
        native_unit_of_measurement=PERCENTAGE,
        is_selected_entity=True,
    ),
)
