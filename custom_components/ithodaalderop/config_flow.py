#!/usr/bin/env python3
"""Config flow component for Itho Add-on.

Author: Jasper Slits
"""
from collections.abc import Mapping
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.selector import selector

from .const import (
    CONF_AUTOTEMP_ROOM1,
    CONF_AUTOTEMP_ROOM2,
    CONF_AUTOTEMP_ROOM3,
    CONF_AUTOTEMP_ROOM4,
    CONF_AUTOTEMP_ROOM5,
    CONF_AUTOTEMP_ROOM6,
    CONF_AUTOTEMP_ROOM7,
    CONF_AUTOTEMP_ROOM8,
    CONF_CVE_TYPE,
    CONF_REMOTE_1,
    CONF_REMOTE_2,
    CONF_REMOTE_3,
    CONF_REMOTE_4,
    CONF_REMOTE_5,
    CONF_USE_AUTOTEMP,
    CONF_USE_REMOTES,
    CONF_USE_WPU,
    CVE_TYPES,
    DOMAIN,
)


class IthoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Itho Config flow."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the Itho Add-on flow."""
        self.config: dict[str, Any] = {}
        self.entry: config_entries.ConfigEntry

    async def async_step_remotes(self, info=None):
        """Configure up to 5 remotes."""
        if info is not None:
            self.config.update(info)
            if self.config[CONF_USE_AUTOTEMP]:
                return await self.async_step_rooms()
            await self.async_set_unique_id("ithoaddon")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title="Itho WiFi Add-on",
                data=self.config
            )

        itho_schema = vol.Schema({
            vol.Required(CONF_REMOTE_1, default="Remote 1"): str,
            vol.Optional(CONF_REMOTE_2, default="Remote 2"): str,
            vol.Optional(CONF_REMOTE_3, default="Remote 3"): str,
            vol.Optional(CONF_REMOTE_4, default="Remote 4"): str,
            vol.Optional(CONF_REMOTE_5, default="Remote 5"): str
        })
        return self.async_show_form(step_id="remotes", data_schema=itho_schema)

    async def async_step_remotes_reconfigure(self, info=None):
        """Reconfigure up to 5 remotes."""
        if info is not None:
            self.config.update(info)
            if self.config[CONF_USE_AUTOTEMP]:
                return await self.async_step_rooms_reconfigure()
            return self.async_update_reload_and_abort(self.entry, data=self.config, reason="reconfigure_successful")

        itho_schema = vol.Schema({
            vol.Required(CONF_REMOTE_1, default=self._get_reconfigure_value(CONF_REMOTE_1, "Remote 1")): str,
            vol.Optional(CONF_REMOTE_2, default=self._get_reconfigure_value(CONF_REMOTE_2, "Remote 2")): str,
            vol.Optional(CONF_REMOTE_3, default=self._get_reconfigure_value(CONF_REMOTE_3, "Remote 3")): str,
            vol.Optional(CONF_REMOTE_4, default=self._get_reconfigure_value(CONF_REMOTE_4, "Remote 4")): str,
            vol.Optional(CONF_REMOTE_5, default=self._get_reconfigure_value(CONF_REMOTE_5, "Remote 5")): str,
        })
        return self.async_show_form(step_id="remotes_reconfigure", data_schema=itho_schema)

    async def async_step_rooms(self, info=None):
        """Configure rooms for autotemp."""
        if info is not None:
            self.config.update(info)
            await self.async_set_unique_id("ithoaddon")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title="Itho WiFi Add-on",
                data=self.config
            )

        itho_schema = vol.Schema({
            vol.Required(CONF_AUTOTEMP_ROOM1, default="Room 1"): str,
            vol.Optional(CONF_AUTOTEMP_ROOM2, default="Room 2"): str,
            vol.Optional(CONF_AUTOTEMP_ROOM3, default="Room 3"): str,
            vol.Optional(CONF_AUTOTEMP_ROOM4, default="Room 4"): str,
            vol.Optional(CONF_AUTOTEMP_ROOM5, default="Room 5"): str,
            vol.Optional(CONF_AUTOTEMP_ROOM6, default="Room 6"): str,
            vol.Optional(CONF_AUTOTEMP_ROOM7, default="Room 7"): str,
            vol.Optional(CONF_AUTOTEMP_ROOM8, default="Room 8"): str,
        })
        return self.async_show_form(step_id="rooms", data_schema=itho_schema)

    def _get_reconfigure_value(self,param,default):
        """Get reconfigure value."""
        if param in self.config:
            return self.config[param]
        return default

    async def async_step_rooms_reconfigure(self, info=None):
        """Reconfigure rooms for autotemp."""
        if info is not None:
            self.config.update(info)
            return self.async_update_reload_and_abort(self.entry, data=self.config, reason="reconfigure_successful")

        itho_schema = vol.Schema({
            vol.Required(CONF_AUTOTEMP_ROOM1, default=self._get_reconfigure_value(CONF_AUTOTEMP_ROOM1,"Room 1")): str,
            vol.Optional(CONF_AUTOTEMP_ROOM2, default=self._get_reconfigure_value(CONF_AUTOTEMP_ROOM2,"Room 2")): str,
            vol.Optional(CONF_AUTOTEMP_ROOM3, default=self._get_reconfigure_value(CONF_AUTOTEMP_ROOM3,"Room 3")): str,
            vol.Optional(CONF_AUTOTEMP_ROOM4, default=self._get_reconfigure_value(CONF_AUTOTEMP_ROOM4,"Room 4")): str,
            vol.Optional(CONF_AUTOTEMP_ROOM5, default=self._get_reconfigure_value(CONF_AUTOTEMP_ROOM5,"Room 5")): str,
            vol.Optional(CONF_AUTOTEMP_ROOM6, default=self._get_reconfigure_value(CONF_AUTOTEMP_ROOM6,"Room 6")): str,
            vol.Optional(CONF_AUTOTEMP_ROOM7, default=self._get_reconfigure_value(CONF_AUTOTEMP_ROOM7,"Room 7")): str,
            vol.Optional(CONF_AUTOTEMP_ROOM8, default=self._get_reconfigure_value(CONF_AUTOTEMP_ROOM8,"Room 8")): str,
        })
        return self.async_show_form(step_id="rooms_reconfigure", data_schema=itho_schema)

    async def async_step_user(self, info=None):
        """Configure main step."""
        if info is not None:
            self.config.update(info)
            if info[CONF_USE_REMOTES]:
                return await self.async_step_remotes()
            if info[CONF_USE_AUTOTEMP]:
                return await self.async_step_rooms()
            await self.async_set_unique_id("ithoaddon")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title="Itho WiFi Add-on",
                data=info
            )
        itho_schema = vol.Schema({
            vol.Required(CONF_CVE_TYPE, default="none"): selector({
                "select": {
                    "options": CVE_TYPES,
                    "multiple": False,
                    "translation_key": "cveselect"
                }
            }),
            vol.Required(CONF_USE_REMOTES, default=False): cv.boolean,
            vol.Required(CONF_USE_WPU, default=False): cv.boolean,
            vol.Required(CONF_USE_AUTOTEMP, default=False): cv.boolean,
        })

        return self.async_show_form(
            step_id="user", data_schema=itho_schema)

    async def async_step_reconfigure(self, info: Mapping[str, Any] | None = None):
        """Reconfigure config flow."""
        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        assert entry
        self.entry = entry
        self.config.update(entry.data)
        if info:
            self.config.update(info)
            if info[CONF_USE_REMOTES]:
                return await self.async_step_remotes_reconfigure()
            if info[CONF_USE_AUTOTEMP]:
                return await self.async_step_rooms_reconfigure()
            return self.async_update_reload_and_abort(self.entry, data=info, reason="reconfigure_successful")

        return await self._redo_configuration(self.entry.data)

    async def _redo_configuration(self, entry_data: Mapping[str, Any]):
        """Reconfigure config flow with schema."""
        self.config.update(entry_data)
        itho_schema = vol.Schema({
            vol.Required(CONF_CVE_TYPE, default=entry_data[CONF_CVE_TYPE]): selector({
                "select": {
                    "options": CVE_TYPES,
                    "multiple": False,
                    "translation_key": "cveselect"
                }
            }),
            vol.Required(CONF_USE_REMOTES, default=entry_data[CONF_USE_REMOTES]): cv.boolean,
            vol.Required(CONF_USE_WPU, default=entry_data[CONF_USE_WPU]): cv.boolean,
            vol.Required(CONF_USE_AUTOTEMP, default=entry_data[CONF_USE_AUTOTEMP]): cv.boolean,
        })

        return self.async_show_form(
            step_id="reconfigure", data_schema=itho_schema)
