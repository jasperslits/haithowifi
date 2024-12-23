"""Definitions for Itho sensors added to MQTT."""

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    PERCENTAGE,
    EntityCategory,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfTime,
)

from .base import IthoSensorEntityDescription

AUTOTEMP_COMM_SPACE_SENSOR_TEMPLATE = IthoSensorEntityDescription(
    json_field="Comm space X (sec)",
    translation_key="comm_space",
    unique_id_template="comm_space_x",
    native_unit_of_measurement=UnitOfTime.SECONDS,
    state_class=SensorStateClass.MEASUREMENT,
    entity_category=EntityCategory.DIAGNOSTIC,
    entity_registry_enabled_default=False,
)

AUTOTEMP_DISTRIBUTOR_VALVE_SENSOR_TEMPLATE = IthoSensorEntityDescription(
    json_field="Distributor X valve Y",
    translation_key="distributor_valve",
    unique_id_template="distributor_x_valve_y",
    entity_category=EntityCategory.DIAGNOSTIC,
    entity_registry_enabled_default=False,
)

AUTOTEMP_MALFUNCTION_VALVE_DECTECTION_DIST_SENSOR_TEMPLATE = (
    IthoSensorEntityDescription(
        json_field="Malfunction valve detection dist X",
        translation_key="malfunction_valve_detection_dist",
        unique_id_template="malfunction_valve_detection_dist_x",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    )
)

AUTOTEMP_ROOM_SENSORS: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field="Room X power % (%)",
        translation_key="power_perc",
        device_class=SensorDeviceClass.POWER_FACTOR,
        native_unit_of_measurement="%",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Room X power kW (kW)",
        translation_key="power_kw",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Room X setp",
        translation_key="setpoint_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Room X temp",
        translation_key="actual_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)

AUTOTEMP_SENSORS: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field="Condition",
        translation_key="condition",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Condition cool",
        translation_key="condition_cool",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Condition off",
        translation_key="condition_off",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Cycle counter (sec)",
        translation_key="cycle_counter",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Desired power (%)",
        translation_key="desired_power",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Error",
        translation_key="error",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    IthoSensorEntityDescription(
        json_field="Heat source",
        translation_key="heat_source",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="LED_Fast",
        translation_key="led_fast",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="LED_On",
        translation_key="led_on",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="LED_Slow",
        translation_key="led_slow",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Mode",
        translation_key="mode",
    ),
    IthoSensorEntityDescription(
        json_field="Outdoor temp (°C)",
        translation_key="outdoor_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Particulars",
        translation_key="particulars",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Rest cycle time (sec)",
        translation_key="rest_cycle_time",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Rest vent time (sec)",
        translation_key="rest_vent_time",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Rest vent time (sec)",
        translation_key="rest_vent_time",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="State cool",
        translation_key="state_cool",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="State hand",
        translation_key="state_hand",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="state hand",
        translation_key="state_hand2",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="State heating",
        translation_key="state_heating",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="State off",
        translation_key="state",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Time active zone too cold (sec)",
        translation_key="time_active_zone_too_cold",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Valve failure detection distributor 1",
        translation_key="valve_failure_detection_distributor_1",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
)

AUTOTEMP_VALVE_SENSOR_TEMPLATE: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field="VX_valve",
        translation_key="v_valve",
        unique_id_template="vx_valve",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Valve failure distributor X",
        translation_key="valve_failure_distributor",
        unique_id_template="valve_failure_distributor_x",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
)
