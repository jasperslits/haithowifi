"""Definitions for Itho sensors added to MQTT."""

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    CONCENTRATION_PARTS_PER_MILLION,
    PERCENTAGE,
    REVOLUTIONS_PER_MINUTE,
    EntityCategory,
    UnitOfElectricCurrent,
    UnitOfTemperature,
    UnitOfVolumeFlowRate,
)

from .definitions import IthoSensorEntityDescription

HRUECO250300SENSORS: tuple[IthoSensorEntityDescription, ...] = (
    IthoSensorEntityDescription(
        json_field="Absolute speed of the fan (%)",
        translation_key="absolute_fanspeed",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    IthoSensorEntityDescription(
        json_field="Current consumption of fan (mA)",
        translation_key="current_consumption_fan",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.MILLIAMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    IthoSensorEntityDescription(
        json_field="Desired capacity (m3/h)",
        translation_key="desired_capacity",
        device_class=SensorDeviceClass.VOLUME_FLOW_RATE,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Desired current consumption of fan (mA)",
        translation_key="desired_consumption_fan",
        device_class=SensorDeviceClass.CURRENT,
        native_unit_of_measurement=UnitOfElectricCurrent.MILLIAMPERE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    IthoSensorEntityDescription(
        json_field="Error number",
        translation_key="error_number",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    IthoSensorEntityDescription(
        json_field="Highest measured CO2 (ppm)",
        translation_key="highest_measured_co2_value",
        native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
        icon="mdi:molecule-co2",
    ),
    IthoSensorEntityDescription(
        json_field="Highest measured RH (%)",
        translation_key="highest_measured_rh_value",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    IthoSensorEntityDescription(
        json_field="Inlet temperature (°C)",
        translation_key="inlet_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Measured blend temperature heated NTC (°C)",
        translation_key="measured_blend_temp_heated",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Measured outside temperature (°C)",
        translation_key="outside_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Measured temperature of mixed outside air (°C)",
        translation_key="mixed_outside_air_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Measured waste temperature heated NTC (°C)",
        translation_key="measured_waste_temp_heated",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Percentage that the bypass valve is open (%)",
        translation_key="bypass_valve_open",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    IthoSensorEntityDescription(
        json_field="Relative fanspeed (%)",
        translation_key="relative_fanspeed",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="RPM of the motor (rpm)",
        translation_key="motor_speed",
        native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Status",
        translation_key="status",
    ),
    IthoSensorEntityDescription(
        json_field="Temperature of the blown out air of the house (°C)",
        translation_key="blown_out_air_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="Temperature of the extracted air (°C)",
        translation_key="extracted_air_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="The desired inlet temperature (°C)",
        translation_key="desired_inlet_temp",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="The flow of the blown air (m3/h)",
        translation_key="flow_blown_air",
        device_class=SensorDeviceClass.VOLUME_FLOW_RATE,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    IthoSensorEntityDescription(
        json_field="The flow of the inflated air (M3/h)",
        translation_key="flow_inflated_air",
        device_class=SensorDeviceClass.VOLUME_FLOW_RATE,
        native_unit_of_measurement=UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # No native_unit_of_measurement available for mass flow
    IthoSensorEntityDescription(
        json_field="The mass flow of the air entering the house (kg/h)",
        translation_key="mass_flow_air_enter_house_kgh",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    # No native_unit_of_measurement available for mass flow
    IthoSensorEntityDescription(
        json_field="The mass flow of the air leaving the house (kg/h)",
        translation_key="mass_flow_air_leaving_house_kgh",
        state_class=SensorStateClass.MEASUREMENT,
    ),
)
