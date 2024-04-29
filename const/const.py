import logging
from enum import IntEnum

DOMAIN = "ithoaddon"
CONF_ID = "id"
CONF_HRU_STATETOPIC = "ithohru/ithostatus"
CONF_WPU_STATETOPIC = "ithowpu/ithostatus"
CONF_AUTOTEMP_STATETOPIC = "ithotemp/ithostatus"
CONF_ENABLED_SENSORS = "ithohru/remotesinfo"

CONF_USE_WPU = "use_wpu"
CONF_USE_HRU = "use_hru"
CONF_USE_AUTOTEMP = "use_autotemp"
CONF_USE_REMOTES = "use_remotes"

CONF_AUTOTEMP_ROOM1 = "Room1"
CONF_AUTOTEMP_ROOM2 = "Room2"
CONF_AUTOTEMP_ROOM3 = "Room3"
CONF_AUTOTEMP_ROOM4 = "Room4"
CONF_AUTOTEMP_ROOM5 = "Room5"
CONF_AUTOTEMP_ROOM6 = "Room6"
CONF_AUTOTEMP_ROOM7 = "Room7"
CONF_AUTOTEMP_ROOM8 = "Room8"

HRU_ACTUAL_MODE = {1: "low", 2: "medium", 3: "high",24: "auto",25: "autonight"}
WPU_STATUS = { 0: "Init", 1: "Off", 2: "CV",3: "Boiler",4: "Cooling",5: "Venting"}
ADDONS = {1: "HRU", 2: "WPU", 3: "AUTOTEMP"}

class AddOnType(IntEnum):
    HRU = 1
    WPU = 2
    AUTOTEMP = 3

_LOGGER = logging.getLogger(__name__)
