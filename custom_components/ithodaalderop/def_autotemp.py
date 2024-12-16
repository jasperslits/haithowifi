"""Definitions for Itho sensors added to MQTT."""

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import EntityCategory, UnitOfPower, UnitOfTemperature

from .definitions import IthoBinarySensorEntityDescription, IthoSensorEntityDescription

AUTOTEMPBINARYSENSORS: tuple[IthoBinarySensorEntityDescription, ...] = (
    IthoBinarySensorEntityDescription(
        json_field="Empty battery ( 0=OK )",
        translation_key="empty_battery",
        device_class=BinarySensorDeviceClass.BATTERY,
        entity_category=EntityCategory.DIAGNOSTIC,
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
