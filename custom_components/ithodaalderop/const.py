"""Consts for Itho add-on."""

import logging

_LOGGER = logging.getLogger(__name__)


################
### SETTINGS ###
################

# QoS 0 – At most once.
# QoS 1 – At least once.
# QoS 2 – Exactly once.
MQTT_DEFAULT_QOS_SUBSCRIBE = 1
MQTT_DEFAULT_QOS_PUBLISH = 1


#################
### CONSTANTS ###
#################

DOMAIN = "ithodaalderop"
MANUFACTURER = "Itho Daalderop"

ADDON_TYPES = {
    "autotemp": "Autotemp",
    "cve": "CVE",
    "noncve": "Non-CVE",
    "wpu": "WPU",
}
ENTITIES_CREATION_MODES = ["only_selected", "all"]

# Both 'hru_eco_250' & 'hru_eco_300' and 'hru_eco_250_300'
# are added for compatibility with both manual and auto-detect
# 'hru_eco_250_300' is removed as manual selection in config-flow
NONCVE_MODELS = {
    "hru_eco": "HRU ECO",
    "hru_eco_200": "HRU ECO 200",
    "hru_eco_250": "HRU ECO 250",
    "hru_eco_300": "HRU ECO 300",
    "hru_eco_250_300": "HRU ECO 250/300",
    "hru_eco_350": "HRU ECO 350",
    "demand_flow": "Demand Flow",
}

AUTODETECT_DEVICE_TYPES = {
    "AutoTemp": {"addon_type": "autotemp"},
    "AutoTemp Basic": {"addon_type": "autotemp"},
    "CVE": {"addon_type": "cve"},
    "CVE-Silent": {"addon_type": "cve"},
    "HRU ECO-fan": {"addon_type": "noncve", "model": "hru_eco"},
    "CVE-SilentExtPlus": {"addon_type": "noncve", "model": "hru_eco_200"},
    "HRU 250-300": {"addon_type": "noncve", "model": "hru_eco_250_300"},
    "HRU 350": {"addon_type": "noncve", "model": "hru_eco_350"},
    "DemandFlow": {"addon_type": "noncve", "model": "demand_flow"},
    "Heatpump": {"addon_type": "wpu"},
}

UNITTYPE_ICONS = {
    "%": "mdi:percent-outline",
    "hum": "mdi:water-percent",
    "rpm": "mdi:speedometer",
}

MQTT_DEFAULT_BASETOPIC = {
    "autotemp": "ithotemp",
    "cve": "ithocve",
    "noncve": "ithohru",
    "wpu": "ithowpu",
}

MQTT_STATETOPIC = {
    "autotemp": "ithostatus",
    "cve": "ithostatus",
    "last_cmd": "lastcmd",
    "noncve": "ithostatus",
    "remote": "remotesinfo",
    "wpu": "ithostatus",
}

MQTT_COMMAND_TOPIC = "cmd"

CONF_ADDON_TYPE = "addontype"
CONF_AUTO_DETECT = "auto_detect"
CONF_ENTITIES_CREATION_MODE = "entities_creation_mode"
CONF_ADVANCED_CONFIG = "advanced_config"
CONF_CUSTOM_BASETOPIC = "custom_basetopic"
CONF_CUSTOM_DEVICE_NAME = "custom_device_name"
CONF_CUSTOM_ENTITY_PREFIX = "custom_entity_prefix"
CONF_NONCVE_MODEL = "noncve_model"

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

HRU_ECO_250_300_ERROR_CODE = {
    0: "No error",
    1: "W01 - Clean Filter",
    2: "W02 - Replace Filter",
    3: "W03 - Fan speed decreased",
    51: "B01 - Temperature outside NOT-OK",
    52: "B02 - Temperature blend NOT-OK",
    53: "B03 - Temperature waste NOT-OK",
    54: "B04 - Temperature return NOT-OK",
    55: "B05 - Temperature supply NOT-OK",
    101: "E01 - Fan is't working",
}

HRU_ECO_350_ACTUAL_MODE = {
    1: "Low",
    2: "Medium",
    3: "High",
    13: "Timer",
    24: "Auto",
    25: "Autonight",
}

# Based on user-experience. No codelist availble in the Itho Servicetool
# For any additions/feedback, please create an issue in the repo of the integration
HRU_ECO_350_GLOBAL_FAULT_CODE = {
    0: "No error",
    7: "Filters dirty",
    11: "(External) Sensor error",
}

HRU_ECO_350_RH_ERROR_CODE = {
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

HRU_ECO_STATUS = {
    0: "Normal",
    1: "Adjust frost valve",
    2: "Decelerate Supply fan",
    3: "Accelerate Exhaust fan",
    4: "Stop supply fan",
}

WPU_STATUS = {
    0: "Init",
    1: "Off",
    2: "CV",
    3: "Boiler",
    4: "Cooling",
    5: "Venting",
}
