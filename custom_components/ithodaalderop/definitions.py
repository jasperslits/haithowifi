"""Definitions for Itho sensors added to MQTT.

A sensor entity represents passive, read-only data provided by a device. It reflects the current state or measurement of something in the environment without directly interacting with or changing the device.
A control entity represents interactive elements that allow the user to send commands or configure a device to change its state or behavior.
A diagnostic entity provides device-specific metadata or operational insights that assist in understanding the device's internal state or functioning but is not directly related to the user's environment.
"""

# TODO: Add support for HRU 200 and HRU 250/300
# Labels (json_fields) can be found @ https://github.com/arjenhiemstra/ithowifi/tree/master/software/NRG_itho_wifi/main/devices

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntityDescription,
)
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
    REVOLUTIONS_PER_MINUTE,
    EntityCategory,
    UnitOfPower,
    UnitOfPressure,
    UnitOfTemperature,
    UnitOfTime,
)


@dataclass(frozen=False)
class IthoSensorEntityDescription(SensorEntityDescription):
    """Sensor entity description for Itho."""

    state: Callable | None = None
    json_field: str | None = None
    key: str | None = None
    icon: str | None = None
    affix: str | None = None
    entity_category: EntityCategory | None = None


@dataclass(frozen=False)
class IthoBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Binary Sensor entity description for Itho."""

    state: Callable | None = None
    json_field: str | None = None
    key: str | None = None
    icon: str | None = None
    icon_off: str | None = None
    icon_on: str | None = None
    affix: str | None = None
    entity_category: EntityCategory | None = None


AUTOTEMPBINARYSENSORS: tuple[IthoBinarySensorEntityDescription, ...] = (
    IthoBinarySensorEntityDescription(
        json_field="Empty battery ( 0=OK )",
        translation_key="empty_battery",
        device_class=BinarySensorDeviceClass.BATTERY,
        entity_category=EntityCategory.DIAGNOSTIC,
        # icon_off="mdi:battery",
        # icon_on="mdi:battery-low",
    ),
)

AUTOTEMPSENSORS: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field="Error",
        translation_key="error",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    IthoSensorEntityDescription(
        json_field="Mode",
        translation_key="mode",
    ),
    IthoSensorEntityDescription(
        json_field="State off",
        translation_key="state",
    ),
)

AUTOTEMPROOMSENSORS: tuple[IthoSensorEntityDescription, ...] = (
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

LASTCMDSENSORS: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field="command",
        translation_key="last_cmd_command",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:cog",
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="source",
        translation_key="last_cmd_source",
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:target",
        entity_registry_enabled_default=False,
    ),
)

HRU350BINARYSENSORS: tuple[IthoBinarySensorEntityDescription, ...] = (
    IthoBinarySensorEntityDescription(
        json_field="Bypass position",
        translation_key="bypass_position",
        device_class=BinarySensorDeviceClass.OPENING,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon_off="mdi:valve-closed",
        icon_on="mdi:valve-open",
    ),
)

HRU350SENSORS: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field="Actual Mode",
        translation_key="actual_mode",
        icon="mdi:knob",
    ),
    IthoSensorEntityDescription(
        json_field="Airfilter counter",
        translation_key="airfilter_counter",
        native_unit_of_measurement=UnitOfTime.HOURS,
        state_class=SensorStateClass.TOTAL_INCREASING,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:counter",
    ),
    IthoSensorEntityDescription(
        json_field="Air Quality (%)",
        translation_key="airquality",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Balance (%)",
        translation_key="balance",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Exhaust fan (RPM)",
        translation_key="actual_exhaust_fan",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Exhaust temp (°C)",
        translation_key="actual_exhaust_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Global fault code",
        translation_key="global_fault_code",
        icon="mdi:alert-circle-outline",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    IthoSensorEntityDescription(
        json_field="Highest received CO2 value (Ppm)",
        translation_key="highest_received_co2_value",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        icon="mdi:molecule-co2",
    ),
    IthoSensorEntityDescription(
        json_field="Highest received RH value (%RH)",
        translation_key="highest_received_rh_value",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Remaining override timer (Sec)",
        translation_key="remaining_override_timer",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:timer-outline",
    ),
    IthoSensorEntityDescription(
        json_field="Supply fan (RPM)",
        translation_key="actual_supply_fan",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Supply temp (°C)",
        translation_key="actual_supply_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)

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

WPUSENSORS: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field="Boiler pump (%)",
        translation_key="boiler_pump_percent",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Boiler temp up (°C)",
        translation_key="boiler_temp_up",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="CV pressure (Bar)",
        translation_key="cv_pressure",
        device_class=SensorDeviceClass.PRESSURE,
        native_unit_of_measurement=UnitOfPressure.BAR,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Cv pump (%)",
        translation_key="cv_pump_percent",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="CV return temp (°C)",
        translation_key="cv_return_temp",
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
        json_field="Flow sensor (lt_hr)",
        translation_key="flow_sensor",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:waves-arrow-right",
    ),
    IthoSensorEntityDescription(
        json_field="Heat demand thermost. (%)",
        translation_key="heat_demand",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Requested room temp (°C)",
        translation_key="requested_room_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Room temp (°C)",
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
        json_field="ECO selected on thermostat",
        translation_key="thermostat",
    ),
    IthoSensorEntityDescription(
        json_field="Temp to source (°C)",
        translation_key="temp_to_source",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Temp from source (°C)",
        translation_key="temp_from_source",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Well pump (%)",
        translation_key="well_pump_percent",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)
