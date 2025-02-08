#!/usr/bin/env python3
"""Config flow component for Itho Add-on.

Author: Jasper Slits
"""

from collections.abc import Mapping
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.selector import selector

from .const import (
    ADDON_TYPES,
    CONF_ADDON_TYPE,
    CONF_ADVANCED_CONFIG,
    CONF_AUTOTEMP_ROOM1,
    CONF_AUTOTEMP_ROOM2,
    CONF_AUTOTEMP_ROOM3,
    CONF_AUTOTEMP_ROOM4,
    CONF_AUTOTEMP_ROOM5,
    CONF_AUTOTEMP_ROOM6,
    CONF_AUTOTEMP_ROOM7,
    CONF_AUTOTEMP_ROOM8,
    CONF_CUSTOM_BASETOPIC,
    CONF_CUSTOM_DEVICE_NAME,
    CONF_CUSTOM_ENTITY_PREFIX,
    CONF_ENTITIES_CREATION_MODE,
    CONF_NONCVE_MODEL,
    CONF_REMOTE_1,
    CONF_REMOTE_2,
    CONF_REMOTE_3,
    CONF_REMOTE_4,
    CONF_REMOTE_5,
    DOMAIN,
    ENTITIES_CREATION_MODES,
    NONCVE_DEVICES,
)
from .sensors.base import (
    get_default_entity_prefix,
    get_default_mqtt_base_topic,
    get_device_model,
    get_entity_prefix,
)


class IthoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Itho Config flow."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the Itho Add-on flow."""
        self.config: dict[str, Any] = {}
        self.entry: config_entries.ConfigEntry

    def _get_reconfigure_value(self, param, default):
        """Get reconfigure value."""
        if param in self.config:
            return self.config[param]
        return default

    async def _set_unique_id(self):
        unique_id = f"itho_wifi_addon_{get_entity_prefix(self.config)}"
        await self.async_set_unique_id(unique_id)

    def get_entry_title(self):
        """Generete title for the entry."""

        addon_type = self.config[CONF_ADDON_TYPE]
        advanced_config = self.config[CONF_ADVANCED_CONFIG]

        title = "Itho WiFi Add-on for "
        if addon_type == "noncve":
            title = title + ADDON_TYPES[addon_type] + " - "

            if advanced_config:
                title = title + self.config[CONF_CUSTOM_DEVICE_NAME]
            else:
                title = title + NONCVE_DEVICES[self.config[CONF_NONCVE_MODEL]]

        elif advanced_config:
            title = title + self.config[CONF_CUSTOM_DEVICE_NAME]

        else:
            title = title + ADDON_TYPES[addon_type]

        return title

    async def async_step_user(self, user_input: Mapping[str, Any] | None = None):
        """Configure main step."""
        if user_input is not None:
            self.config.update(user_input)
            if user_input[CONF_ADDON_TYPE] == "autotemp":
                return await self.async_step_rooms()
            if user_input[CONF_ADDON_TYPE] == "cve":
                return await self.async_step_remotes()
            if user_input[CONF_ADDON_TYPE] == "noncve":
                return await self.async_step_noncve_model()
            if user_input.get(CONF_ADVANCED_CONFIG, False):
                return await self.async_step_advanced_config()

            await self._set_unique_id()
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title=f"Itho WiFi Add-on for {ADDON_TYPES[self.config[CONF_ADDON_TYPE]]}",
                data=user_input,
            )

        itho_schema = vol.Schema(
            {
                vol.Required(CONF_ADDON_TYPE): selector(
                    {
                        "select": {
                            "options": list(ADDON_TYPES.keys()),
                            "multiple": False,
                            "translation_key": "addonselect",
                        }
                    }
                ),
                vol.Required(CONF_ENTITIES_CREATION_MODE): selector(
                    {
                        "select": {
                            "options": ENTITIES_CREATION_MODES,
                            "multiple": False,
                            "translation_key": "entities_creation_modes",
                        }
                    }
                ),
                vol.Required(CONF_ADVANCED_CONFIG): selector({"boolean": {}}),
            }
        )

        return self.async_show_form(step_id="user", data_schema=itho_schema)

    async def async_step_rooms(self, user_input: Mapping[str, Any] | None = None):
        """Configure rooms for autotemp."""
        if user_input is not None:
            self.config.update(user_input)
            if self.config[CONF_ADVANCED_CONFIG]:
                return await self.async_step_advanced_config()

            await self._set_unique_id()
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=self.get_entry_title(),
                data=self.config,
            )

        itho_schema = vol.Schema(
            {
                vol.Required(CONF_AUTOTEMP_ROOM1, default="Room 1"): str,
                vol.Optional(CONF_AUTOTEMP_ROOM2, default="Room 2"): str,
                vol.Optional(CONF_AUTOTEMP_ROOM3, default="Room 3"): str,
                vol.Optional(CONF_AUTOTEMP_ROOM4, default="Room 4"): str,
                vol.Optional(CONF_AUTOTEMP_ROOM5, default="Room 5"): str,
                vol.Optional(CONF_AUTOTEMP_ROOM6, default="Room 6"): str,
                vol.Optional(CONF_AUTOTEMP_ROOM7, default="Room 7"): str,
                vol.Optional(CONF_AUTOTEMP_ROOM8, default="Room 8"): str,
            }
        )
        return self.async_show_form(
            step_id="rooms", data_schema=itho_schema, last_step=True
        )

    async def async_step_noncve_model(
        self, user_input: Mapping[str, Any] | None = None
    ):
        """Configure Non-CVE (HRU) Device."""
        if user_input is not None:
            self.config.update(user_input)
            return await self.async_step_remotes()

        itho_schema = vol.Schema(
            {
                vol.Required(CONF_NONCVE_MODEL): selector(
                    {
                        "select": {
                            "options": list(NONCVE_DEVICES.keys()),
                            "multiple": False,
                            "translation_key": "noncve_model_select",
                        }
                    }
                ),
            }
        )

        return self.async_show_form(step_id="noncve_model", data_schema=itho_schema)

    async def async_step_remotes(self, user_input: Mapping[str, Any] | None = None):
        """Configure up to 5 remotes."""
        if user_input is not None:
            self.config.update(user_input)
            if self.config[CONF_ADVANCED_CONFIG]:
                return await self.async_step_advanced_config()

            await self._set_unique_id()
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=self.get_entry_title(),
                data=self.config,
            )

        itho_schema = vol.Schema(
            {
                vol.Required(CONF_REMOTE_1, default="Remote 1"): str,
                vol.Optional(CONF_REMOTE_2, default="Remote 2"): str,
                vol.Optional(CONF_REMOTE_3, default="Remote 3"): str,
                vol.Optional(CONF_REMOTE_4, default="Remote 4"): str,
                vol.Optional(CONF_REMOTE_5, default="Remote 5"): str,
            }
        )
        return self.async_show_form(
            step_id="remotes", data_schema=itho_schema, last_step=True
        )

    async def async_step_advanced_config(
        self, user_input: Mapping[str, Any] | None = None
    ):
        """Advanced configuration for multiple devices that would use the same MQTT basetopic."""
        if user_input is not None:
            self.config.update(user_input)
            await self._set_unique_id()
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=self.get_entry_title(),
                data=self.config,
            )

        itho_schema = vol.Schema(
            {
                vol.Required(
                    CONF_CUSTOM_BASETOPIC,
                    default=get_default_mqtt_base_topic(self.config),
                ): str,
                vol.Required(
                    CONF_CUSTOM_ENTITY_PREFIX,
                    default=get_default_entity_prefix(self.config),
                ): str,
                vol.Required(
                    CONF_CUSTOM_DEVICE_NAME,
                    default=get_device_model(self.config),
                ): str,
            }
        )
        return self.async_show_form(
            step_id="advanced_config", data_schema=itho_schema, last_step=True
        )

    async def async_step_reconfigure(self, user_input: Mapping[str, Any] | None = None):
        """Reconfigure config flow."""
        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        assert entry
        self.entry = entry
        self.config.update(self.entry.data)

        if user_input is not None:
            self.config.update(user_input)
            if self.entry.data[CONF_ADDON_TYPE] == "autotemp":
                return await self.async_step_rooms_reconfigure()
            if self.entry.data[CONF_ADDON_TYPE] in ["cve", "noncve"]:
                return await self.async_step_remotes_reconfigure()

            return self.async_update_reload_and_abort(
                self.entry, data=self.config, reason="reconfigure_successful"
            )

        itho_schema = vol.Schema(
            {
                vol.Required(CONF_ENTITIES_CREATION_MODE): selector(
                    {
                        "select": {
                            "options": ENTITIES_CREATION_MODES,
                            "multiple": False,
                            "translation_key": "entities_creation_modes",
                        }
                    }
                ),
            }
        )

        return self.async_show_form(step_id="reconfigure", data_schema=itho_schema)

    async def async_step_rooms_reconfigure(
        self, user_input: Mapping[str, Any] | None = None
    ):
        """Reconfigure rooms for autotemp."""
        if user_input is not None:
            self.config.update(user_input)
            return self.async_update_reload_and_abort(
                self.entry, data=self.config, reason="reconfigure_successful"
            )

        itho_schema = vol.Schema(
            {
                vol.Required(
                    CONF_AUTOTEMP_ROOM1,
                    default=self._get_reconfigure_value(CONF_AUTOTEMP_ROOM1, "Room 1"),
                ): str,
                vol.Optional(
                    CONF_AUTOTEMP_ROOM2,
                    default=self._get_reconfigure_value(CONF_AUTOTEMP_ROOM2, "Room 2"),
                ): str,
                vol.Optional(
                    CONF_AUTOTEMP_ROOM3,
                    default=self._get_reconfigure_value(CONF_AUTOTEMP_ROOM3, "Room 3"),
                ): str,
                vol.Optional(
                    CONF_AUTOTEMP_ROOM4,
                    default=self._get_reconfigure_value(CONF_AUTOTEMP_ROOM4, "Room 4"),
                ): str,
                vol.Optional(
                    CONF_AUTOTEMP_ROOM5,
                    default=self._get_reconfigure_value(CONF_AUTOTEMP_ROOM5, "Room 5"),
                ): str,
                vol.Optional(
                    CONF_AUTOTEMP_ROOM6,
                    default=self._get_reconfigure_value(CONF_AUTOTEMP_ROOM6, "Room 6"),
                ): str,
                vol.Optional(
                    CONF_AUTOTEMP_ROOM7,
                    default=self._get_reconfigure_value(CONF_AUTOTEMP_ROOM7, "Room 7"),
                ): str,
                vol.Optional(
                    CONF_AUTOTEMP_ROOM8,
                    default=self._get_reconfigure_value(CONF_AUTOTEMP_ROOM8, "Room 8"),
                ): str,
            }
        )
        return self.async_show_form(
            step_id="rooms_reconfigure", data_schema=itho_schema, last_step=True
        )

    async def async_step_remotes_reconfigure(
        self, user_input: Mapping[str, Any] | None = None
    ):
        """Reconfigure up to 5 remotes."""
        if user_input is not None:
            self.config.update(user_input)
            return self.async_update_reload_and_abort(
                self.entry, data=self.config, reason="reconfigure_successful"
            )

        itho_schema = vol.Schema(
            {
                vol.Required(
                    CONF_REMOTE_1,
                    default=self._get_reconfigure_value(CONF_REMOTE_1, "Remote 1"),
                ): str,
                vol.Optional(
                    CONF_REMOTE_2,
                    default=self._get_reconfigure_value(CONF_REMOTE_2, "Remote 2"),
                ): str,
                vol.Optional(
                    CONF_REMOTE_3,
                    default=self._get_reconfigure_value(CONF_REMOTE_3, "Remote 3"),
                ): str,
                vol.Optional(
                    CONF_REMOTE_4,
                    default=self._get_reconfigure_value(CONF_REMOTE_4, "Remote 4"),
                ): str,
                vol.Optional(
                    CONF_REMOTE_5,
                    default=self._get_reconfigure_value(CONF_REMOTE_5, "Remote 5"),
                ): str,
            }
        )
        return self.async_show_form(
            step_id="remotes_reconfigure", data_schema=itho_schema, last_step=True
        )
