"""Consts for Itho add-on."""

import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "ithodaalderop"

MANUFACTURER = "Itho Daalderop"

ADDON_TYPES = {
    "noncve": "HRU",
    "cve": "CVE",
    "autotemp": "Autotemp",
    "wpu": "WPU",
}

CVE_TYPES = {
    "noncve": ["noncve", "mdi:fan"],
    "cve": ["cve", "mdi:fan"],
}

UNITTYPE_ICONS = {
    "%": "mdi:percent-outline",
    "hum": "mdi:water-percent",
    "rpm": "mdi:speedometer",
}

MQTT_BASETOPIC = {
    "cve": "ithocve",
    "noncve": "ithohru",
    "wpu": "ithowpu",
    "autotemp": "ithotemp",
}

MQTT_STATETOPIC = {
    "cve": "ithostatus",
    "noncve": "ithostatus",
    "wpu": "ithostatus",
    "autotemp": "ithostatus",
    "remote": "remotesinfo",
}

CONF_ADDON_TYPE = "addontype"

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
CONF_REMOTE_3 = "remote3"
CONF_REMOTE_4 = "remote4"
CONF_REMOTE_5 = "remote5"


AUTOTEMP_ERROR = {
    0: "No errors",
    1: "No communication with MFT for 30 minutes",
    2: "No communication with MFT for 30 minutes roomtherm",
    3: "No communication with slave 1 for 30 minutes",
    4: "No communication with slave 2 for 30 minutes",
    5: "Configuration not properly completed",
    6: "Valve not detected",
    7: "Valve control failed",
    8: "One or more RT battery empty",
    9: "Battery master thermostat empty",
    10: "Master thermostat has a defect sensor",
    11: "One of the Room thermostats has a defect sensor",
    12: "Bathroom sensor defect",
    13: "Controller is in manual mode",
}

AUTOTEMP_MODE = {
    0: "Boot up",
    1: "Initialize",
    2: "Commissioning",
    3: "Running",
    4: "Configuration",
    5: "Manual operation",
}

NONCVE_ACTUAL_MODE = {
    1: "low",
    2: "medium",
    3: "high",
    13: "timer",
    24: "auto",
    25: "autonight",
}

# Based on user-experience. No codelist availble in the Itho Servicetool
# For any additions/feedback, please create an issue in the repo of the integration
NONCVE_GLOBAL_FAULT_CODE = {
    0: "No error",
    7: "Filters dirty",
    11: "(External) Sensor error",
}

NONCVE_RH_ERROR_CODE = {
    239: "Not Available",
    240: "Shorted Sensor",
    241: "Open Sensor",
    242: "Not Available Error",
    243: "Out Of Range High",
    244: "Out Of Range Low",
    245: "Not Reliable",
    246: "Reserved Error",
    247: "Reserved Error",
    248: "Reserved Error",
    249: "Reserved Error",
    250: "Reserved Error",
    251: "Reserved Error",
    252: "Reserved Error",
    253: "Reserved Error",
    254: "Reserved Error",
    255: "Unknown Error",
}

WPU_STATUS = {
    0: "Init",
    1: "Off",
    2: "CV",
    3: "Boiler",
    4: "Cooling",
    5: "Venting",
}
