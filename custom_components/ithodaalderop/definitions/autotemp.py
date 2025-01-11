"""Definitions for Itho Autotemp sensors added to MQTT."""

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    PERCENTAGE,
    EntityCategory,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfTime,
)

from .base import IthoBinarySensorEntityDescription, IthoSensorEntityDescription

AUTOTEMP_BINARYSENSORS: tuple[IthoBinarySensorEntityDescription, ...] = (
    IthoBinarySensorEntityDescription(
        json_field="Empty battery ( 0=OK )",
        key="empty_battery",
        device_class=BinarySensorDeviceClass.BATTERY,
        entity_category=EntityCategory.DIAGNOSTIC,
        # icon_off="mdi:battery",
        # icon_on="mdi:battery-low",
        is_selected_entity=True,
    ),
)

AUTOTEMP_COMM_SPACE_SENSOR_TEMPLATE = IthoSensorEntityDescription(
    json_field="Comm space X (sec)",
    key="comm_space",
    unique_id_template="comm_space_x",
    native_unit_of_measurement=UnitOfTime.SECONDS,
    state_class=SensorStateClass.MEASUREMENT,
    entity_category=EntityCategory.DIAGNOSTIC,
    entity_registry_enabled_default=False,
)

AUTOTEMP_DISTRIBUTOR_VALVE_SENSOR_TEMPLATE = IthoSensorEntityDescription(
    json_field="Distributor X valve Y",
    key="distributor_valve",
    unique_id_template="distributor_x_valve_y",
    entity_category=EntityCategory.DIAGNOSTIC,
    entity_registry_enabled_default=False,
)

AUTOTEMP_MALFUNCTION_VALVE_DECTECTION_DIST_SENSOR_TEMPLATE = (
    IthoSensorEntityDescription(
        json_field="Malfunction valve detection dist X",
        key="malfunction_valve_detection_dist",
        unique_id_template="malfunction_valve_detection_dist_x",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    )
)

AUTOTEMP_ROOM_SENSORS: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field="Room X power % (%)",
        key="power_perc",
        device_class=SensorDeviceClass.POWER_FACTOR,
        native_unit_of_measurement="%",
        state_class=SensorStateClass.MEASUREMENT,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="Room X power kW (kW)",
        key="power_kw",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="Room X setp",
        key="setpoint_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="Room X temp",
        key="actual_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        is_selected_entity=True,
    ),
)

AUTOTEMP_SENSORS: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field="Condition",
        key="condition",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Condition cool",
        key="condition_cool",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Condition off",
        key="condition_off",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Cycle counter (sec)",
        key="cycle_counter",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Desired power (%)",
        key="desired_power",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="Error",
        key="error",
        entity_category=EntityCategory.DIAGNOSTIC,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="Heat source",
        key="heat_source",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="LED_Fast",
        key="led_fast",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="LED_On",
        key="led_on",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="LED_Slow",
        key="led_slow",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Mode",
        key="mode",
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="Outdoor temp (°C)",
        key="outdoor_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="Particulars",
        key="particulars",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Rest cycle time (sec)",
        key="rest_cycle_time",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Rest vent time (sec)",
        key="rest_vent_time",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="State cool",
        key="state_cool",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="State hand",
        key="state_hand",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="state hand",
        key="state_hand2",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="State heating",
        key="state_heating",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="State off",
        key="state",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        is_selected_entity=True,
    ),
    IthoSensorEntityDescription(
        json_field="Time active zone too cold (sec)",
        key="time_active_zone_too_cold",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Valve failure detection distributor 1",
        key="valve_failure_detection_distributor_1",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
)

AUTOTEMP_VALVE_SENSOR_TEMPLATE: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field="VX_valve",
        key="v_valve",
        unique_id_template="vx_valve",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Valve failure distributor X",
        key="valve_failure_distributor",
        unique_id_template="valve_failure_distributor_x",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
)
