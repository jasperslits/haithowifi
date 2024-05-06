## Home Assistant sensor component/integration for Itho Wifi
Requires add-on from https://github.com/arjenhiemstra/ithowifi and MQTT integration with Home Assistant. 

Tested with WPU 5G, 2 CO2 sensors, HRU-350 (non-CVE) devices

### Use-case
Full auto-discovery from the add-on to Home Assistant is the best experience but as this is not there yet, this add-on should eliminate the manual creation via YAML of sensors for:
* Non-CVE like Actual mode, supply temp, Supply / Exhaust RPM
* CVE like humidity, temperature, speed
* Autotemp like power kW, power %, set point temp, actual temp per room
* CO2 sensors for supported remotes
* WPU like pump percentage, boiler temp, from / to source temps etc

It creates the commony used sensors and uses a predefined MQTT state topic to distinct the devices.

This custom integration should become obsolete once full auto-discovery has the same capabilities. 

### What works / should work
1. Create WPU sensors
2. Create NONCVE / HRU sensors
3. Create CVE sensors
4. Create up to two Remotes (CO2 sensors)
5. Create Auto temp sensors

Overall: translations are available in English for now. NL to follow

## How to install
1. In the Add-On from Arjen: Update the add-on MQTT configuration to use ithohru for NON-CVE, ithowpu for Heatpump/WPU and ithotemp for Autotemp. 
2. On the system running Home Assistant: Create /usr/share/hassio/homeassistant/custom_components/itho
3. Git clone or download / extract the content of this repo to that folder
4. Restart Home Assistant
5. Go to Integrations
6. Add Itho integration
7. Enable the devices you want to configure

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
* Submit project for HACS integration
* Add reconfigure to config flow












