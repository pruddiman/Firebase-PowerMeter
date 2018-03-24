# Firebase Power Meter
The Firebase Power Meter is a python script written for the Raspberry Pi. It uses an I2C Current sensor to monitor Current. 

# Hardware Requirements
- Raspberry Pi Model 3 (B, B+)
- [Control Everything I2C Current Sensor](https://store.ncd.io/shop/?fwp_product_type=energy-monitors&fwp_interface=i2c-interface)
- [Control Everything I2C Shield for Raspberry Pi](https://store.ncd.io/?fwp_product_type=i2c-adapters&fwp_platform=raspberry-pi-3)
- 5v and 12v PSU (this can be one unit or multiple)
- Enclosure for all the components

# Executing
> cd /opt
> git clone --depth=0 https://github.com/pruddiman/Firebase-PowerMeter ./powermeter
> cd ./powermeter
> python main.py 
