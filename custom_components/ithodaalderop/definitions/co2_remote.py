"""Definitions for Itho CO2 Remote sensors added to MQTT."""

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import CONCENTRATION_PARTS_PER_MILLION

from .base_definitions import IthoSensorEntityDescription

REMOTE_SENSOR_TEMPLATE = IthoSensorEntityDescription(
    key="remote",
    device_class=SensorDeviceClass.CO2,
    native_unit_of_measurement=CONCENTRATION_PARTS_PER_MILLION,
    state_class=SensorStateClass.MEASUREMENT,
    is_selected_entity=True,
)
