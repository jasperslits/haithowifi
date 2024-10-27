## Home Assistant sensor component/integration for Itho Wifi
Requires WiFi add-on from https://github.com/arjenhiemstra/ithowifi and [MQTT](https://www.home-assistant.io/integrations/mqtt/) integration with Home Assistant. 

This simplifies the integration by creating the sensors for the various Itho Daalderop devices: Heatpump WPU 5G, HRU-350 and related devices, CVE boxes, Autotemp units for floor heating. 
For best user experience it should be used with the auto-discovery for the CVE / non-CVE devices in the add-on. 

This custom component has no affiliation with the Itho Daalderop company or with Arjen Hiemstra's Itho WiFi add-on.

Note: The 'add-on' here in the context is the ESP32 add-on to the Itho Daalderop units, not an Add-on in Home Assistant. 

### Use-case
Full auto-discovery from the WiFi add-on to Home Assistant is the best experience but as this is not there yet, this integration should eliminate the manual creation via YAML of sensors for:
* Non-CVE like Actual mode, Supply Temp, Supply / Exhaust RPM, Bypass 
* CVE like Humidity, Temperature, Speed
* Autotemp like Power kW, Power %, Set Point Temp, Actual Temp per Room
* CO2 sensors for supported remotes
* WPU like Pump Percentage, Boiler Temp, From / To Source Temps, Operating Mode etc

It creates the commonly used sensors and uses a predefined MQTT state topic to distinct the devices.

This custom integration should become obsolete once full auto-discovery via the Itho Add-on has the same capabilities. 

### Available sensors
| Device | Sensor | Attributes |
|---|---|---|
| **Autotemp** |||
|| Room X power % (%) ||
|| Room X power kW (kW) ||
|| Room X setpoint ||
|| Room X temp ||
| **CVE** |||
|| Fan setpoint (rpm) ||
|| Humidity ||
|| Temperature ||
|| Ventilation setpoint (%) ||
| **NONCVE (HRU)** |||
|| Actual Mode ||
|| Air Quality (%) ||
|| Airfilter counter |Last Maintenance|
||| Next Maintenance Estimate |
|| Balance (%) ||
|| Bypass position ||
|| Exhaust fan (RPM) ||
|| Exhaust temp (°C) ||
|| Global fault code | Description |
|| Remaining override timer (Sec) ||
|| Supply fan (RPM) ||
|| Supply temp (°C) ||
| **WPU** |||
|| Boiler pump (%) ||
|| Boiler temp up (°C) ||
|| CV pressure (Bar) ||
|| Cv pump (%) ||
|| CV return temp (°C) ||
|| Flow sensor (lt_hr) ||
|| Heat demand thermost. (%) ||
|| Status ||
|| Temp from source (°C) ||
|| Temp to source (°C) ||
|| Requested room temp (°C) ||
|| Room temp (°C) ||
|| Well pump (%) ||

Missing a sensor? Feel free to create an [issue](https://github.com/jasperslits/haithowifi/issues)

### Prerequisites
1. Working WiFi add-on connected to the Itho device(s)
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

## How to install
1. In the Add-On from Arjen: Update the add-on MQTT configuration and set MQTT Base Topic to `ithohru` for NON-CVE, `ithowpu` for Heatpump/WPU and `ithotemp` for Autotemp. 
2. On the system running Home Assistant: Create /usr/share/hassio/homeassistant/custom_components/ithodaalderop
3. Install the component via HACS custom repo. See https://hacs.xyz/docs/faq/custom_repositories/ and use Integration in the dropdown and https://github.com/jasperslits/haithowifi/ as name **OR** 
4. Git clone or download the content to custom_components in the /usr/share/hassio/homeassistant/custom_components/ithodaalderop directory 
5. Restart Home Assistant
6. Go to Integrations
7. Search for Itho Add-on integration
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
* Submit project for HACS integration. In progress via https://github.com/hacs/default/pull/2494
* Add reconfigure to config flow
