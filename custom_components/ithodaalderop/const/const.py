import logging
from enum import IntEnum


class AddOnType(IntEnum):
    CVE = 1
    WPU = 2
    AUTOTEMP = 3
    REMOTES = 4
    NONCVE = 5


HRU_ACTUAL_MODE = {
    1: "low",
    2: "medium",
    3: "high",
    13: "timer",
    24: "auto",
    25: "autonight"
}

WPU_STATUS = {
    0: "Init",
    1: "Off",
    2: "CV",
    3: "Boiler",
    4: "Cooling",
    5: "Venting"
}

ADDONS = {
    1: "CVE",
    2: "WPU",
    3: "AUTOTEMP",
    4: "REMOTES",
    5: "NONCVE"
}

CVE_TYPES = {
    "none": ["none", "mdi:fan"],
    "noncve": ["noncve", "mdi:fan"],
    "cve": ["cve", "mdi:fan"]
}

UNITTYPE_ICONS = {
    "rpm": "mdi:speedometer",
    "hum": "mdi:water-percent",
    "%": "mdi:percent-outline"
}

DOMAIN = "ithodaalderop"
CONF_ID = "id"
MQTT_STATETOPIC = {"hru": "ithohru/ithostatus", "wpu": "ithowpu/ithostatus", "remotes": "ithohru/remotesinfo","autotemp": "ithotemp/ithostatus" }
CONF_ENABLED_SENSORS = "ithohru/remotesinfo"
CONF_CVE_TYPE = "cvetype"
CONF_USE_WPU = "use_wpu"
CONF_USE_AUTOTEMP = "use_autotemp"
CONF_USE_REMOTES = "use_remotes"

CONF_AUTOTEMP_ROOM1 = "room1"
CONF_AUTOTEMP_ROOM2 = "room2"
CONF_AUTOTEMP_ROOM3 = "room3"
CONF_AUTOTEMP_ROOM4 = "room4"
CONF_AUTOTEMP_ROOM5 = "room5"
CONF_AUTOTEMP_ROOM6 = "room6"
CONF_AUTOTEMP_ROOM7 = "room7"
CONF_AUTOTEMP_ROOM8 = "room8"

CONF_REMOTE_1 = "remote1"
CONF_REMOTE_2 = "remote2"


_LOGGER = logging.getLogger(__name__)
