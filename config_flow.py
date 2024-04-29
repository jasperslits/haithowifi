#!/usr/bin/env python3
"""
Config flow component for Itho Add-on
Author: Jasper Slits
"""
import pprint
from homeassistant.helpers.selector import selector
from homeassistant.helpers import config_validation as cv
from homeassistant import config_entries
from .const.const import (
    _LOGGER,
    DOMAIN,
    CONF_ID,
    CONF_USE_HRU,
    CONF_USE_AUTOTEMP,
    CONF_USE_WPU,
    CONF_USE_REMOTES
)

import voluptuous as vol

class IthoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, info=None):
        
        if info is not None:
            if info[CONF_USE_AUTOTEMP]: 
                _LOGGER.warning("Use autotemp")
            await self.async_set_unique_id(info["id"])
            self._abort_if_unique_id_configured()
            return self.async_create_entry(
                title="Itho Add-on for " + info["id"],
                data=info
            )

        itho_schema = vol.Schema({
        vol.Required(CONF_ID, default="home"): str,
        vol.Optional(CONF_USE_HRU,default=False): cv.boolean,
        vol.Optional(CONF_USE_REMOTES,default=False): cv.boolean,
        vol.Optional(CONF_USE_WPU,default=False): cv.boolean,
        vol.Optional(CONF_USE_AUTOTEMP,default=False): cv.boolean,
        })
        
        return self.async_show_form(
              step_id="user", data_schema=itho_schema)

  # TODO: Create separate form
  #       vol.Optional(CONF_AUTOTEMP_ROOM1,default="Room 1"): str,
  #       vol.Optional(CONF_AUTOTEMP_ROOM2,default="Room 2"): str,
  #       vol.Optional(CONF_AUTOTEMP_ROOM3,default="Room 3"): str,
  #       vol.Optional(CONF_AUTOTEMP_ROOM4,default="Room 4"): str,
  #       vol.Optional(CONF_AUTOTEMP_ROOM5,default="Room 5"): str,
  #       vol.Optional(CONF_AUTOTEMP_ROOM6,default="Room 6"): str,
  #       vol.Optional(CONF_AUTOTEMP_ROOM7,default="Room 7"): str,
  #       vol.Optional(CONF_AUTOTEMP_ROOM8,default="Room 8"): str,
        

