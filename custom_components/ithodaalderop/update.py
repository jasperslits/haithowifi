"""Update entity for Home Assistant."""

from __future__ import annotations

import json

from homeassistant.components import mqtt
from homeassistant.components.update import (
    UpdateDeviceClass,
    UpdateEntity,
    UpdateEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    ADDON_TYPES,
    CONF_ADDON_TYPE,
    CONF_NONCVE_MODEL,
    DOMAIN,
    MANUFACTURER,
    MQTT_BASETOPIC,
    NONCVE_DEVICES,
)

UPDATE_DESCRIPTION = UpdateEntityDescription(
    key="firmware",
    device_class=UpdateDeviceClass.FIRMWARE,
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """One update sensor per device."""

    async_add_entities([IthoHAUpdate(UPDATE_DESCRIPTION, config_entry)])


class IthoHAUpdate(UpdateEntity):
    """Update entity for Itho addon."""

    _installedversion = ""
    _latestversion = ""
    _mqttbase = ""

    def __init__(
        self,
        entity_description: UpdateEntityDescription,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""

        self._mqttbase = MQTT_BASETOPIC[config_entry.data[CONF_ADDON_TYPE]]

        model = ADDON_TYPES[config_entry.data[CONF_ADDON_TYPE]]
        if config_entry.data[CONF_ADDON_TYPE] == "noncve":
            model = model + " - " + NONCVE_DEVICES[config_entry.data[CONF_NONCVE_MODEL]]

        self._attr_name = model

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.data[CONF_ADDON_TYPE])},
            manufacturer=MANUFACTURER,
            model=model,
            name=ADDON_TYPES[config_entry.data[CONF_ADDON_TYPE]],
        )

        self.entity_description = entity_description

    async def async_added_to_hass(self) -> None:
        """Subscribe to MQTT events."""

        @callback
        def message_received(message):
            """Handle new MQTT messages."""
            payload = json.loads(message.payload)
            self._installedversion = payload["add-on_fwversion"]
            self._latestversion = payload["add-on_latest_fw"]
            self.async_write_ha_state()

        await mqtt.async_subscribe(
            self.hass, f"{self._mqttbase}/deviceinfo", message_received, 1
        )

    @property
    def installed_version(self) -> str | None:
        """HA Itho version on the device."""
        return self._installedversion

    @property
    def latest_version(self) -> str:
        """HA Itho stable version."""
        return self._latestversion

    @property
    def title(self) -> str:
        """Return title for the update."""
        return "Stable release of the Itho Wifi add-on only"

    @property
    def release_url(self) -> str:
        """Returns Github Repo link."""
        return (
            "https://github.com/arjenhiemstra/ithowifi/releases/tag/Version-"
            + self._latestversion
        )
