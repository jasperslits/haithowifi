"""Definitions for Itho sensors added to MQTT."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass
)
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntityDescription
)
from homeassistant.const import (
    UnitOfTemperature,
    UnitOfTime,
    UnitOfPower,
    UnitOfPressure,
    CONCENTRATION_PARTS_PER_MILLION,
    REVOLUTIONS_PER_MINUTE,
    PERCENTAGE
)

from .const import MQTT_STATETOPIC


@dataclass(frozen=False)
class IthoSensorEntityDescription(SensorEntityDescription):
    """Sensor entity description for Itho."""

    state: Callable | None = None
    json_field: str | None = None
    icon: str | None = None


@dataclass(frozen=False)
class IthoBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Binary Sensor entity description for Itho."""

    state: Callable | None = None
    json_field: str | None = None
    icon: str | None = None
    icon_off: str | None = None
    icon_on: str | None = None


WPUSENSORS: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field="Boiler pump (%)",
        key=MQTT_STATETOPIC["wpu"],
        translation_key="boiler_pump_percent",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Boiler temp up (°C)",
        key=MQTT_STATETOPIC["wpu"],
        translation_key="boiler_temp_up",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="CV pressure (Bar)",
        key=MQTT_STATETOPIC["wpu"],
        translation_key="cv_pressure",
        device_class=SensorDeviceClass.PRESSURE,
        native_unit_of_measurement=UnitOfPressure.BAR,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Cv pump (%)",
        key=MQTT_STATETOPIC["wpu"],
        translation_key="cv_pump_percent",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="CV return temp (°C)",
        key=MQTT_STATETOPIC["wpu"],
        translation_key="cv_return_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Flow sensor (lt_hr)",
        key=MQTT_STATETOPIC["wpu"],
        translation_key="flow_sensor",
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:waves-arrow-right",
    ),
    IthoSensorEntityDescription(
        json_field="Heat demand thermost. (%)",
        key=MQTT_STATETOPIC["wpu"],
        translation_key="heat_demand",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Requested room temp (°C)",
        key=MQTT_STATETOPIC["wpu"],
        translation_key="requested_room_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Room temp (°C)",
        key=MQTT_STATETOPIC["wpu"],
        translation_key="room_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Status",
        key=MQTT_STATETOPIC["wpu"],
        translation_key="status",
    ),
    IthoSensorEntityDescription(
        json_field="Temp to source (°C)",
        key=MQTT_STATETOPIC["wpu"],
        translation_key="temp_to_source",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Temp from source (°C)",
        key=MQTT_STATETOPIC["wpu"],
        translation_key="temp_from_source",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Well pump (%)",
        key=MQTT_STATETOPIC["wpu"],
        translation_key="well_pump_percent",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)

AUTOTEMPSENSORS: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field="Room X power % (%)",
        key=MQTT_STATETOPIC["autotemp"],
        translation_key="Room X power % (%)",
        device_class=SensorDeviceClass.POWER_FACTOR,
        native_unit_of_measurement="%",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Room X power kW (kW)",
        key=MQTT_STATETOPIC["autotemp"],
        translation_key="Room X power kW",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Room X setp",
        key=MQTT_STATETOPIC["autotemp"],
        translation_key="Room X setpoint temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Room X temp",
        key=MQTT_STATETOPIC["autotemp"],
        translation_key="Room X actual temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)

CVESENSORS: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field="Fan setpoint (rpm)",
        key=MQTT_STATETOPIC["hru"],
        translation_key="fan_setpoint_rpm",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="hum",
        key=MQTT_STATETOPIC["hru"],
        translation_key="humidity",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="temp",
        key=MQTT_STATETOPIC["hru"],
        translation_key="temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Ventilation setpoint (%)",
        key=MQTT_STATETOPIC["hru"],
        translation_key="ventilation_setpoint_percentage",
        native_unit_of_measurement=PERCENTAGE,
    ),
)

NONCVEBINARYSENSORS: tuple[IthoBinarySensorEntityDescription, ...] = (
    IthoBinarySensorEntityDescription(
        json_field="Bypass position",
        key=MQTT_STATETOPIC["hru"],
        translation_key="bypass_position",
        device_class=BinarySensorDeviceClass.OPENING,
        icon_off="mdi:valve-closed",
        icon_on="mdi:valve-open",
    ),
)

NONCVESENSORS: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field="Actual Mode",
        key=MQTT_STATETOPIC["hru"],
        translation_key="actual_mode",
        icon="mdi:knob"
    ),
    IthoSensorEntityDescription(
        json_field="Airfilter counter",
        key=MQTT_STATETOPIC["hru"],
        translation_key="airfilter_counter",
        native_unit_of_measurement=UnitOfTime.HOURS,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:counter",
    ),
    IthoSensorEntityDescription(
        json_field="Air Quality (%)",
        key=MQTT_STATETOPIC["hru"],
        translation_key="airquality",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Balance (%)",
        key=MQTT_STATETOPIC["hru"],
        translation_key="balance",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Exhaust fan (RPM)",
        key=MQTT_STATETOPIC["hru"],
        translation_key="actual_exhaust_fan",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Exhaust temp (°C)",
        key=MQTT_STATETOPIC["hru"],
        translation_key="actual_exhaust_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Global fault code",
        key=MQTT_STATETOPIC["hru"],
        translation_key="global_fault_code",
    ),
    IthoSensorEntityDescription(
        json_field="Highest received CO2 value (Ppm)",
        key=MQTT_STATETOPIC["hru"],
        translation_key="highest_received_co2_value",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        icon="mdi:molecule-co2",
    ),
    IthoSensorEntityDescription(
        json_field="Highest received RH value (%RH)",
        key=MQTT_STATETOPIC["hru"],
        translation_key="highest_received_rh_value",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Remaining override timer (Sec)",
        key=MQTT_STATETOPIC["hru"],
        translation_key="remaining_override_timer",
        native_unit_of_measurement=UnitOfTime.SECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:timer-outline",
    ),
    IthoSensorEntityDescription(
        json_field="Supply fan (RPM)",
        key=MQTT_STATETOPIC["hru"],
        translation_key="actual_supply_fan",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Supply temp (°C)",
        key=MQTT_STATETOPIC["hru"],
        translation_key="actual_supply_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)
