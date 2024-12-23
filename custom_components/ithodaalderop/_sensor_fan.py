"""Sensor class for handling Fan sensors."""

from datetime import datetime, timedelta
import json

from homeassistant.components import mqtt
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from ._sensor_base import IthoBaseSensor
from .const import (
    HRU_ECO_250_300_ERROR_CODE,
    HRU_ECO_350_ACTUAL_MODE,
    HRU_ECO_350_GLOBAL_FAULT_CODE,
    HRU_ECO_350_RH_ERROR_CODE,
    HRU_ECO_STATUS,
)
from .definitions.base import IthoSensorEntityDescription


class IthoSensorFan(IthoBaseSensor):
    """Representation of a Itho add-on sensor that is updated via MQTT."""

    _attr_has_entity_name = True
    entity_description: IthoSensorEntityDescription

    _extra_state_attributes = None

    def __init__(
        self,
        description: IthoSensorEntityDescription,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(description, config_entry)

    @property
    def extra_state_attributes(self) -> list[str] | None:
        """Return the state attributes."""
        return self._extra_state_attributes

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""

        @callback
        def message_received(message):
            """Handle new MQTT messages."""
            payload = json.loads(message.payload)
            json_field = self.entity_description.json_field
            if json_field not in payload:
                value = None
            else:
                value = payload[json_field]
                # HRU ECO 350
                if json_field == "Actual Mode":
                    self._extra_state_attributes = {"Code": value}
                    value = HRU_ECO_350_ACTUAL_MODE.get(value, "Unknown mode")

                # HRU ECO 350
                if json_field == "Air Quality (%)":
                    _error_description = "Unknown error code"
                    if isinstance(value, (int, float)) and float(value) > 100:
                        _error_description = "Unknown error"
                        value = None

                    self._extra_state_attributes = {
                        "Error Description": _error_description,
                    }

                # HRU ECO 350 / HRU ECO
                if json_field in ["Airfilter counter", "Air filter counter"]:
                    _last_maintenance = ""
                    _next_maintenance_estimate = ""
                    if str(value).isnumeric():
                        _last_maintenance = (
                            datetime.now() - timedelta(hours=int(value))
                        ).date()
                        _next_maintenance_estimate = (
                            datetime.now() + timedelta(days=180, hours=-int(value))
                        ).date()
                    else:
                        _last_maintenance = "Invalid value"

                    self._extra_state_attributes = {
                        "Last Maintenance": _last_maintenance,
                        "Next Maintenance Estimate": _next_maintenance_estimate,
                    }

                # HRU ECO 250/300
                if json_field == "Error number":
                    _description = ""
                    if str(value).isnumeric():
                        _error_description = HRU_ECO_250_300_ERROR_CODE.get(
                            int(value), _description
                        )

                    self._extra_state_attributes = {
                        "Description": _description,
                    }

                # HRU ECO 350
                if json_field == "Global fault code":
                    _description = "Unknown fault code"
                    if str(value).isnumeric():
                        _description = HRU_ECO_350_GLOBAL_FAULT_CODE.get(
                            int(value), _description
                        )

                    self._extra_state_attributes = {
                        "Description": _description,
                    }

                # HRU ECO 350
                if json_field == "Highest received RH value (%RH)":
                    _error_description = ""
                    if isinstance(value, (int, float)) and float(value) > 100:
                        _error_description = HRU_ECO_350_RH_ERROR_CODE.get(
                            int(value), "Unknown error"
                        )
                        value = None

                    self._extra_state_attributes = {
                        "Error Description": _error_description,
                    }

                # HRU ECO
                if json_field == "Status":
                    self._extra_state_attributes = {
                        "Code": value,
                    }

                    _description = "Unknown status"
                    if str(value).isnumeric():
                        _description = HRU_ECO_STATUS.get(int(value), _description)
                    value = _description

            self._attr_native_value = value
            self.async_write_ha_state()

        await mqtt.async_subscribe(
            self.hass, self.entity_description.key, message_received, 1
        )
