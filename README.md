## Home Assistant sensor component/integration for Itho Wifi
Requires WiFi add-on from https://github.com/arjenhiemstra/ithowifi and [MQTT](https://www.home-assistant.io/integrations/mqtt/) integration with Home Assistant. 

This simplifies the integration by creating the sensors for the various Itho Daalderop devices: Heatpump WPU 5G, HRU-350 and related devices, CVE boxes, Autotemp units for floor heating. 
Combine this integration with the Home Assistant auto-discovery in the MQTT configuration for the CVE / non-CVE devices in the add-on. 

This custom component has no affiliation with the Itho Daalderop company or with Arjen Hiemstra's Itho WiFi add-on.
Note: The 'add-on' here in the context is the ESP32 add-on to the Itho Daalderop units, not an Add-on in Home Assistant. 

### What can be configured via this Integration
1. Heatpump WPU sensors
2. NONCVE / HRU sensors
3. CVE sensors
4. Up to 5 remotes for monitoring CO2 levels
5. Up to 8 autotemp rooms using custom room names instead of Room 1, Room 2

### Not (yet) supported
The fan entity is not supported yet. To add this to Home Assistant enable the Auto-discovery in Arjen's module under MQTT settings or manually configured it. 
See https://github.com/arjenhiemstra/ithowifi/wiki/Home-Assistant the wiki for details

### Use-case
Full auto-discovery from the WiFi add-on to Home Assistant is the best experience but as this is not there yet, this integration should eliminate the manual creation via YAML of sensors for:
* Non-CVE like Actual mode, Supply Temp, Supply / Exhaust RPM, Bypass 
* CVE like Humidity, Temperature, Speed
* Autotemp like Power kW, Power %, Set Point Temp, Actual Temp per Room
* CO2 concencration for supported remotes
* WPU like Pump Percentage, Boiler Temp, From / To Source Temps, Operating Mode etc

It creates a device and commonly used sensors and uses a predefined MQTT state topic to distinct the devices.

### Available sensors
| Device | Sensor | Attributes |
|---|---|---|
| **Autotemp** |||
|| Empty battery ||
|| Error | Code |
|| Mode | Code |
|| Room X power % (%) ||
|| Room X power kW (kW) ||
|| Room X setpoint ||
|| Room X temp ||
|| Status | Code |
| **CVE** |||
|| Error ||
|| Fan Setpoint (rpm) ||
|| Fan Speed (rpm) ||
|| Filter dirty ||
|| Humidity ||
|| Temperature ||
|| Total Operating Time ||
|| Ventilation setpoint (%) ||
| **NONCVE (HRU)** |||
|| Actual Mode | Code |
|| Air Quality (%) ||
|| Airfilter counter | Last Maintenance |
||| Next Maintenance Estimate |
|| Balance (%) ||
|| Bypass position ||
|| Exhaust fan (RPM) ||
|| Exhaust temp (°C) ||
|| Global fault code | Description |
|| Highest received CO2 value (Ppm) (disabled by default) ||
|| Highest received RH value (%RH) (disabled by default) | Error Description |
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
2. [MQTT HA Integration](https://www.home-assistant.io/integrations/mqtt/)
3. State topics for MQTT like table below

| Device  | MQTT base topic   | 
|---|---|
| Autotemp  | ithotemp  |
| CVE  | ithocve  |
| HRU  | ithohru  | 
| WPU  | ithowpu  |

## How to install
1. In the Add-On from Arjen: Update the add-on MQTT configuration and set MQTT Base Topic as per below above
2. On the system running Home Assistant: Create /usr/share/hassio/homeassistant/custom_components/ithodaalderop
3. Install the component via HACS custom repo. See https://hacs.xyz/docs/faq/custom_repositories/ and use Integration in the dropdown and https://github.com/jasperslits/haithowifi/ as name **OR** 
4. Git clone or download the content to custom_components in the /usr/share/hassio/homeassistant/custom_components/ithodaalderop directory 
5. Restart Home Assistant
6. Go to Integrations
7. Search for Itho Add-on integration
8. Add an entry for each device

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
* Add Integration to HACS default (waiting for https://github.com/hacs/default/pull/2494)
* Explore adding Fan without autodiscovery


