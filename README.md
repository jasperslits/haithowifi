## Home Assistant sensor component/integration for Itho Wifi
Requires add-on from https://github.com/arjenhiemstra/ithowifi and MQTT integration with Home Assistant. 

This simplifies the integration by creating the sensors for the various Itho Daalderop devices: Heatpump WPU 5G, HRU-350 and related devices, CVE boxes, Autotemp units for floor heating. 
For best user experience it should be used with the auto-discovery for the CVE / non-CVE devices in the add-on. 

This custom component has no relation with the Itho Daalderop company or with Arjen Hiemstra's Itho Wifi add-on.

Note: The 'add-on' here in the context is the ESP32 add-on to the Itho Daalderop units, not an Add-on in Home Assistant. 

### Use-case
Full auto-discovery from the add-on to Home Assistant is the best experience but as this is not there yet, this add-on should eliminate the manual creation via YAML of sensors for:
* Non-CVE like Actual mode, supply temp, Supply / Exhaust RPM
* CVE like humidity, temperature, speed
* Autotemp like power kW, power %, set point temp, actual temp per room
* CO2 sensors for supported remotes
* WPU like pump percentage, boiler temp, from / to source temps, operating mode etc

It creates the commony used sensors and uses a predefined MQTT state topic to distinct the devices.

This custom integration should become obsolete once full auto-discovery via the Itho Add-on has the same capabilities. 

### Prerequisites
1. Working add-on connected to the Itho device(s)
2. State topics for MQTT like table below

| Device  | MQTT base topic   | 
|---|---|
| HRU  | ithohru  | 
| WPU  | ithowpu  |
| CVE  | ithohru  |
| Autotemp  | ithotemp  |
| Remotes | ithohru |

### What works / should work
1. Create Heatpump WPU sensors
2. Create NONCVE / HRU Fan sensors
3. Create CVE fan sensors
4. Create up to two Remotes for monitoring CO2 levels
5. Create Auto temp sensors and manage rooms

Overall: translations are available in English only for now. Dutch to follow. 

## How to install
1. In the Add-On from Arjen: Update the add-on MQTT configuration to use ithohru for NON-CVE, ithowpu for Heatpump/WPU and ithotemp for Autotemp. 
2. On the system running Home Assistant: Create /usr/share/hassio/homeassistant/custom_components/ithodaalderop
3. Install the component via HACS custom repo. See https://hacs.xyz/docs/faq/custom_repositories/ and use Integration in the dropdown and https://github.com/jasperslits/haithowifi/ as name **OR** 
4. Git clone or download the content to custom_components in the /usr/share/hassio/homeassistant/custom_components/ithodaalderop directory 
5. Restart Home Assistant
6. Go to Integrations
7. Add Itho add-on integration
8. Enable the devices you want to configure

### Screenshots
1. Add integration
<img width="599" alt="image" src="https://github.com/jasperslits/haithowifi/assets/30024136/8c2a7d99-a770-44de-bb9c-52bdd9b0740f">

2. Define remotes for CO2 monitoring
<img width="478" alt="image" src="https://github.com/jasperslits/haithowifi/assets/30024136/cc075268-0b94-42e9-9789-1bb0c4d28069">

3. Define rooms for autotemp
<img width="410" alt="image" src="https://github.com/jasperslits/haithowifi/assets/30024136/73d8c25d-5364-4b59-af09-8e74c83d0468">

4. Created sensors
<img width="984" alt="image" src="https://github.com/jasperslits/haithowifi/assets/30024136/652e97ad-d9f0-43a3-991b-840af8935356">

5. CVE sensors
<img width="983" alt="image" src="https://github.com/jasperslits/haithowifi/assets/30024136/45b33a5f-50bc-476c-9a78-8df7af71fdd1">


### TODO:
* Add binary sensors for bypass of HRU
* Update of NL translations
* Submit project for HACS integration. In progress via https://github.com/hacs/default/pull/2494
* Add reconfigure to config flow












