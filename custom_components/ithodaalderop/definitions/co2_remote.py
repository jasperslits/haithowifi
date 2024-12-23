"""Definitions for Itho sensors added to MQTT."""

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import CONCENTRATION_PARTS_PER_MILLION

from .base import IthoSensorEntityDescription

REMOTE_SENSOR_TEMPLATE = IthoSensorEntityDescription(
    translation_key="remote",
    device_class=SensorDeviceClass.CO2,
    native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
    state_class=SensorStateClass.MEASUREMENT,
)
