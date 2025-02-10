#!/usr/bin/env python3
"""Fan component for Itho.

Author: Benjamin
"""

import json

from homeassistant.components import mqtt
from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_OFF, STATE_ON
from homeassistant.core import HomeAssistant, callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import _LOGGER

PRESET_MODES = [
    "Low",
    "Medium",
    "High",
    "Auto",
    "Autonight",
    "Timer 10",
    "Timer 20",
    "Timer 30",
    "Timer",
]


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the MQTT fan from configuration.yaml."""
    async_add_entities([MqttFan(hass, config_entry)])


class MqttFan(FanEntity):
    """Representation of an MQTT-controlled fan."""

    def __init__(self, hass: HomeAssistant, config: ConfigEntry) -> None:
        """Initialize the fan."""
        super().__init__()
        self.hass = hass
        self._name = "Ventilator"
        self._unique_id = "f8be29e7-363a-4cdf-a5b1-aeb8e170ec49"
        self._state = None
        self._preset_mode = None
        self._available_preset_modes = PRESET_MODES

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""
        await mqtt.async_subscribe(
            self.hass, "ithohru/lwt", self._state_message_received
        )
        await mqtt.async_subscribe(
            self.hass, "ithohru/ithostatus", self._preset_mode_message_received
        )

    @property
    def name(self):
        """Return the name of the fan."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique ID of the fan."""
        return self._unique_id

    @property
    def should_poll(self):
        """No polling needed for MQTT fan."""
        return False

    @property
    def is_on(self):
        """Return true if the fan is on."""
        return self._state == STATE_ON

    @property
    def preset_modes(self):
        """Return the available preset modes."""
        return self._available_preset_modes

    @property
    def preset_mode(self):
        """Return the current preset mode."""
        return self._preset_mode

    @property
    def supported_features(self) -> FanEntityFeature:
        """Return the list of supported features."""
        return FanEntityFeature.PRESET_MODE

    async def async_set_preset_mode(self, preset_mode):
        """Set the fan preset mode."""
        if preset_mode in PRESET_MODES:
            if preset_mode == "Low":
                preset_command = "low"
            elif preset_mode == "Medium":
                preset_command = "medium"
            elif preset_mode == "High":
                preset_command = "high"
            elif preset_mode == "Timer":
                preset_command = "timer"
            elif preset_mode == "Timer 10":
                preset_command = "timer1"
            elif preset_mode == "Timer 20":
                preset_command = "timer2"
            elif preset_mode == "Timer 30":
                preset_command = "timer3"
            elif preset_mode == "Auto":
                preset_command = "auto"
            elif preset_mode == "Autonight":
                preset_command = "autonight"

            payload = json.dumps({"vremote": preset_command})
            await mqtt.async_publish(self.hass, "ithohru/cmd", payload)
            self._preset_mode = preset_mode
            self.async_write_ha_state()
        else:
            _LOGGER.warning("Invalid preset mode: %s", preset_mode)

    @callback
    def _state_message_received(self, msg):
        """Handle state update via MQTT."""
        if msg.payload == "online":
            self._state = STATE_ON
        else:
            self._state = STATE_OFF
        self.async_write_ha_state()

    @callback
    def _preset_mode_message_received(self, msg):
        """Handle preset mode update via MQTT."""
        try:
            data = json.loads(msg.payload)
            actual_mode = int(data.get("Actual Mode", -1))

            if actual_mode == 1:
                self._preset_mode = "Low"
            elif actual_mode == 2:
                self._preset_mode = "Medium"
            elif actual_mode == 3:
                self._preset_mode = "High"
            elif actual_mode == 13:
                self._preset_mode = "Timer"
            elif actual_mode == 24:
                self._preset_mode = "Auto"
            elif actual_mode == 25:
                self._preset_mode = "Autonight"
            else:
                self._preset_mode = actual_mode

            self.async_write_ha_state()
        except ValueError:
            _LOGGER.error("Invalid JSON received for preset mode: %s", msg.payload)
