# Table of Contents
- [Home Assistant sensor component/integration for Itho Wifi](#home-assistant-sensor-componentintegration-for-itho-wifi))
  - [What can be configured via this Integration](#what-can-be-configured-via-this-integration)
  - [Differences with the add-on's Home Assistant MQTT Discovery](#differences-with-the-itho-wifi-add-on-home-assistant-mqtt-discovery)
  - [Use-case](#use-case)
  - [Advanced configuration](#advanced-configuration)
  - [Available entities](#available-entities)
  - [Why don't I see all entities?](#why-dont-i-see-all-entities)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Install via HACS (recommended)](#install-via-hacs-recommended)
  - [Manual install](#manual-install)
  - [Upgrading from 1.4 or below (+ keeping history)](#upgrading-from-14-or-below--keeping-history)
- [Screenshots](#screenshots)
- [Help us improve!](#help-us-improve)

# Home Assistant sensor component/integration for Itho Wifi
This integration for Home Assistant provides a simple configuration screen for the MQTT based "Itho Wifi add-on" from https://github.com/arjenhiemstra/ithowifi
This simplifies the integration by creating the sensors for the various Itho Daalderop devices: Heatpump WPU 5G, HRU units, CVE boxes, Autotemp units for floor heating. 

This custom component has no affiliation with the Itho Daalderop company or with Arjen Hiemstra's Itho WiFi add-on.

## What can be configured via this Integration
1. Autotemp sensors with up to 10 autotemp rooms using custom room names instead of Room 1, Room 2
2. Heatpump WPU sensors
3. CVE sensors
4. NON-CVE / HRU sensors
5. Up to 5 remotes for monitoring CO2 levels for CVE/NON-CVE (HRU)

## Differences with the Itho WiFi add-on Home Assistant MQTT Discovery
This integration does not support the MQTT fan entity while this is provided via the MQTT Discovery. 
To add this to Home Assistant enable Home Assistant MQTT Discovery in Arjen's module under MQTT settings or manually configure it in YAML.
See the [wiki](https://github.com/arjenhiemstra/ithowifi/wiki/Home-Assistant) for details. 

Custom autotemp roomnames and CO2 remote names are also unique to this integration.  

Additional differences include the translations in Dutch, support for other Itho devices besides a fan, value translations for e.g. status. 

## Use-case
This integration should eliminate the manual creation via YAML of sensors for:
* Non-CVE (HRU) like Actual mode, Supply Temp, Supply / Exhaust RPM, Bypass 
* CVE like Humidity, Temperature, Speed
* Autotemp like Power kW, Power %, Set Point Temp, Actual Temp per Room
* CO2 concencration for supported remotes
* WPU like Pump Percentage, Boiler Temp, From / To Source Temps, Operating Mode etc


## Advanced configuration
The integration has an option for advanced configuration. This can be enable during setup which allows for the customization of one or more of the following settings:
- MQTT base topic
- Prefix used for the created entities
- Device name

This can be used to created multiple Home Assistant integration entries for the same device-type (for example, for users with multiple CVE's). Or just if you want to customize the entry to your own liking.

## Available entities
The integration creates a device and sensors and uses a predefined MQTT state topic to distinct the devices. At first only a (by the authors) selected group of entities will be created. If you want to create all available entities for your device, you need to re-configure the integation entry:

Navigate to [integrations](https://my.home-assistant.io/create-link/?redirect=integrations) and find the `Itho WiFi Add-on`. Click the three dots of the entry you want edit:

![image](https://github.com/user-attachments/assets/4d46443b-777e-4899-a49f-5cc9ada1d92c)

Click `Reconfigure` and reconfigure the created entities

![image](https://github.com/user-attachments/assets/3c608faf-60c3-489a-97bf-ddc35af7e329)

## Why don't I see all entities?
Some sensor are disabled by default. Follow these instructions to enable an entity.

Click `xx entities not shown` within the device or just navigate to the entity directly

![image](https://github.com/user-attachments/assets/2a72a81d-7007-410e-af52-9ba43e88352c)

Click the `cogwheel` icon

![image](https://github.com/user-attachments/assets/3c7c89a8-b847-48b1-a7ae-d272da72c552)

Click `enable`

![image](https://github.com/user-attachments/assets/64f7b234-648d-4e25-adeb-996c0d6a7ef8)

# Installation

## Prerequisites
1. Working WiFi add-on connected to the Itho device(s) ([buy](https://www.nrgwatch.nl/))
2. [Official HA MQTT Integration](https://www.home-assistant.io/integrations/mqtt/) configured and connected to the MQTT broker. 
3. In the Itho WiFi add-on under 'MQTT' the `MQTT base topic` should be configured like the table below:

| Device  | MQTT base topic   | 
|---|---|
| Autotemp  | ithotemp  |
| CVE  | ithocve  |
| HRU  | ithohru  | 
| WPU  | ithowpu  |

## Install via HACS (recommended)
1. Install HACS by following [these](https://www.hacs.xyz/docs/use/) steps
2. Install the component via HACS custom repository. See [here](https://hacs.xyz/docs/faq/custom_repositories/) and use Integration in the dropdown and https://github.com/jasperslits/haithowifi/ as name 

## Manual install
1. Using a HA file editor like [`Studio Code Server`](https://github.com/hassio-addons/addon-vscode/blob/main/vscode/DOCS.md) or [`File Editor`](https://www.home-assistant.io/common-tasks/os/#installing-and-using-the-file-editor-add-on), create a folder /usr/share/hassio/homeassistant/custom_components/ithodaalderop
2. Git clone this repository or download the content to custom_components in the /usr/share/hassio/homeassistant/custom_components/ithodaalderop directory 
3. Restart Home Assistant
4. Go to Integrations
5. Search for Itho Add-on integration
6. Add an entry for each device

## Upgrading from 1.4 or below (+ keeping history)
Version `2.0.0` includes major improvements that changes the entity id's for all entities within a device. Due to this change old entities will no longer be provided by the integration and no longer work. You will need to reconfigure the integration:
1. Navigate to `Settings` -> `Devices & Services` and find `Itho WiFi Add-on`.
2. For each entry press ` ⠇ ` (three dots) and press `Delete`.
3. Reconfigure a new entry by pressing `ADD DEVICE` for each Itho Wifi Add-on you own.

In order to keep the history from your old entities follow this process for each entity:


>_According to https://www.home-assistant.io/blog/2023/04/05/release-20234/#database-scalability_:
>
>It may take a while to complete background data migration, depending on the size of your stored data. To ensure Home Assistant keeps history when renaming an entity, wait 24 hours after upgrading before renaming.

1. Rename the entity to the entity-id of the old entity. (For example, change `sensor.itho_hru_actual_exhaust_fan` back to `sensor.noncve_actual_exhaust_fan`)
2. **Wait 24 hours**
3. Rename the entity back to the new naming scheme. The history should now be kept with your new entity-id

# Screenshots
## Add integration
![image](https://github.com/user-attachments/assets/6203c5b0-0cd4-44fe-bf8a-e6e5bec8c8c7)

## Define remotes for CO2 monitoring
<img width="612" alt="image" src="https://github.com/user-attachments/assets/d9d2dca1-254c-450b-84a8-a71f5afee608">

## Define rooms for autotemp
<img width="612" alt="image" src="https://github.com/user-attachments/assets/cd554cac-3cc7-4c5f-b6fd-7efc7c63b256">

## Created devices
<img width="1031" alt="image" src="https://github.com/user-attachments/assets/2235a880-79e0-4a0e-80f3-134f10af7208">

## Created HRU sensors and two remotes
<img width="463" alt="image" src="https://github.com/user-attachments/assets/f8ebf3cd-c2a9-43a0-96bd-00d235b6d6ca">

## CVE sensors
<img src="https://github.com/user-attachments/assets/feef6706-28ac-48db-897f-ea780e5d38f9">

## Autotemp Control Unit + Connected Sensors
<img width="322" alt="image" src="https://github.com/user-attachments/assets/bcad60cc-5635-4ef1-b792-2d08452d8b33">

## Advanced configuration
![image](https://github.com/user-attachments/assets/d8072051-5a9c-4ff8-bc7a-a26866d4b7ab)


### TODO:
* Add Integration to HACS default (waiting for https://github.com/hacs/default/pull/2494)
* Explore adding Fan without autodiscovery

# Help us improve!
As we don't own all Itho devices ourselves, we don't always know the exact meaning and usage of an available sensor. You can help us improve the integration by providing feedback about:
- Translations
- Binary sensors. When a sensor provides only binary data (on/off, open/close, ...)
- Should a sensor be within the 'selected' group of sensors
- Should a sensor be enabled by default
- ...

Feel free to create an [issue](https://github.com/jasperslits/haithowifi/issues)!
