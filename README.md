## Home Assistant sensor component/integration for Itho Wifi
Requires add-on from https://github.com/arjenhiemstra/ithowifi
Tested with WPU 5G and HRU-350 (non-CVE) devices

### Use-case
Full auto-discovery from the add-on to Home Assistant is the best experience but as this is not there yet, this add-on should eliminate the manual creation via YAML of sensors for:
* CVE / Non-CVE like Actual mode, supply temp, RPM
* Autotemp like power kW, power %, set point temp, actual temp per room
* CO2 sensors for supported remotes
* WPU like pump percentage, boiler temp, from / to source temps etc

It creates the commony used sensors and uses a predefined MQTT state topic to distinct the devies. 

### What works / should work
1. Create WPU sensors
2. Create NONCVE sensors
3. Create up to two Remotes (CO2 sensors)
4. Autotemp config flow (but doesnt create sensors yet)

## How to install
1. Create /usr/share/hassio/homeassistant/custom_components/itho
2. Git clone or download / extract the content of this repo to that folder
3. Restart Home Assistant
4. Go to Integrations
5. Add Itho integration

### Screenshots
1. Add integration
<img width="599" alt="image" src="https://github.com/jasperslits/haithowifi/assets/30024136/8c2a7d99-a770-44de-bb9c-52bdd9b0740f">

2. Define remotes for CO2 monitoring
<img width="478" alt="image" src="https://github.com/jasperslits/haithowifi/assets/30024136/cc075268-0b94-42e9-9789-1bb0c4d28069">

3. Created sensors
<img width="984" alt="image" src="https://github.com/jasperslits/haithowifi/assets/30024136/652e97ad-d9f0-43a3-991b-840af8935356">

### TODO:
* Create 4 sensors per room for autotemp for power kW, power %, set point temp, actual temp
* Create CVE sensors (e.g. speed). 
* Add project to HACS









