## Home Assistant sensor component/integration for Itho Wifi
Requires WiFi add-on from https://github.com/arjenhiemstra/ithowifi and [MQTT](https://www.home-assistant.io/integrations/mqtt/) integration with Home Assistant. 

This simplifies the integration by creating the sensors for the various Itho Daalderop devices: Heatpump WPU 5G, HRU-350 and related devices, CVE boxes, Autotemp units for floor heating. 
Combine this integration with the Home Assistant auto-discovery in the MQTT configuration for the CVE / non-CVE devices in the add-on. 

This integration is intended for standard domestic set ups: 1 WPU, 1 CVE or HRU unit, up to 10 rooms connected to autotemp and up to 5 CO2 remotes. More complex setups should be managed via YAML and are out of scope.  

This custom component has no affiliation with the Itho Daalderop company or with Arjen Hiemstra's Itho WiFi add-on.
Note: The 'add-on' here in the context is the ESP32 add-on to the Itho Daalderop units, not an Add-on in Home Assistant. 

### Upgrading from 1.4 or below (+ keeping history):
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

### What can be configured via this Integration
1. Heatpump WPU sensors
2. NONCVE / HRU sensors
3. CVE sensors
4. Up to 5 remotes for monitoring CO2 levels
5. Up to 10 autotemp rooms using custom room names instead of Room 1, Room 2

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
|| Last Command (disabled by default) ||
|| Last Command Source (disabled by default) ||
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
|| Last Command (disabled by default) ||
|| Last Command Source (disabled by default) ||
| **WPU** |||
|| Boiler pump (%) ||
|| Boiler temp up (°C) ||
|| CV pressure (Bar) ||
|| Cv pump (%) ||
|| CV return temp (°C) ||
|| Error ||
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
<img width="606" alt="image" src="https://github.com/user-attachments/assets/5e32a3e3-a06b-4be0-9681-6a640f486abc">

2. Define remotes for CO2 monitoring
<img width="612" alt="image" src="https://github.com/user-attachments/assets/d9d2dca1-254c-450b-84a8-a71f5afee608">

3. Define rooms for autotemp
<img width="612" alt="image" src="https://github.com/user-attachments/assets/cd554cac-3cc7-4c5f-b6fd-7efc7c63b256">

4. Created devices
<img width="1031" alt="image" src="https://github.com/user-attachments/assets/2235a880-79e0-4a0e-80f3-134f10af7208">

5. Created HRU sensors and two remotes
<img width="463" alt="image" src="https://github.com/user-attachments/assets/f8ebf3cd-c2a9-43a0-96bd-00d235b6d6ca">

6. CVE sensors
<img src="https://github.com/user-attachments/assets/feef6706-28ac-48db-897f-ea780e5d38f9">

7. Autotemp Control Unit + Connected Sensors
<img width="322" alt="image" src="https://github.com/user-attachments/assets/bcad60cc-5635-4ef1-b792-2d08452d8b33">

### TODO:
* Add Integration to HACS default (waiting for https://github.com/hacs/default/pull/2494)
* Explore adding Fan without autodiscovery


