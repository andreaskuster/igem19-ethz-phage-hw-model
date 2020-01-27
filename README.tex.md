# <img src="doc/igem-ethz-logo.svg" alt="iGEM ETHZ Logo" width="75"/> iGEM ETH Zurich - <img src="doc/igem19-ethz-logo.svg" alt="iGEM 19 ETHZ Logo" width="120"/> Libraries for Personalized Phage Therapy [![Build Status](https://travis-ci.com/andreaskuster/igem19-ethz-phage-hw-model.svg?branch=master)](https://travis-ci.com/andreaskuster/igem19-ethz-phage-hw-model) [![Coverage Status](https://coveralls.io/repos/github/andreaskuster/igem19-ethz-phage-hw-model/badge.svg?branch=master)](https://coveralls.io/github/andreaskuster/igem19-ethz-phage-hw-model?branch=master) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


## Project Abstract
Antibiotic resistant pathogens are a major threat to global health. Emerging superbugs are rapidly becoming resistant to available antibiotics, while the discovery of new antibiotics is falling behind. Phage therapy offers a potential solution that has achieved remarkable successes. However, it is limited by the number of pathogens that can be targeted by available natural phages. To address this limitation, we aim to increase the range of phage specificities. Host specificity is influenced by the affinity of the phage’s binding protein to the bacterial surface. We developed a system that integrates random codons in phage genomes at any locus of interest. This allows for the formation of phage libraries with novel binding proteins that alter the host spectrum. Our bioreactor selects and evolves the best variants. The observed phage-host interactions can be used to further improve library design. Our system could be the basis for personalized treatment of bacterial infections. 
We are currently testing three approaches to generate these libraries.
* Yeast assembly: a plasmid containing the T7 genome is assembled by homologous recombination in yeast and a library of randomized oligos is inserted into variable region of tail fiber protein.
* Recombineering: A randomised sequence present on a plasmid is inserted into the tail fiber gene in vivo by using E. coli's homologous recombination machinery.
* In vitro: The tail fiber variable regions are ligated to the T7 genome in vitro by Gibson assembly. 

## Project Trailer
[![T007 - License to Lyse - iGEM 2019 ETH Zurich - Trailer](https://img.youtube.com/vi/lpeFW6eoZ5g/maxresdefault.jpg)](https://www.youtube.com/watch?v=lpeFW6eoZ5g?autoplay=1)


## Hardware Reactor Abstract
<img src="doc/reactor.jpg" alt="Hardware Reactor"/>

To ensure the clinical relevance of our library, the rapid selection of the best phage variants is necessary and ensured by our bioreactor. Three flasks for cell growth each have integrated temperature control and peristaltic pumps on top of continuous OD measurement using our self-built OD sensors. This enables the cultivation of bacteria under controlled OD profiles. Real-time data from ongoing experiments is fed into our model to predict host concentrations and adjust growth conditions accordingly. User-friendly software allows the implementation of other experimental setups with custom parameters and monitoring mechanisms. Remote access and alerts permit long-term experiments. Our prototype was of great use for our own long-term and large volume experiments which led to multiple iterations of hardware and software improvements. To allow others to benefit from our design, we extensively documented the hardware and software. This bioreactor offers a cost-efficient solution to perform complex experimental designs with ease.



## Table of content
* [Case Study](#case-study-recombineering-library-experiment)
    * [Setup](#experiment-setup)
    * [Result](#result)
* [Hardware Reactor](#hardware-reactor)
    * [Hardware Overview](#hardware-overview)
    * [Hardware Components](#hardware-components)
    * [Software Overview](#software-overview)
        * [Online Optical Density Sensor](#)
        * [Reactor Temperature Control](#)
* [Software Model](#software-model)
    * [General](#general)
    * [Yeast Assembly](#phage-hw-model-1-yeast-assembly)
    * [Recombineering](#phage-hw-model-2-recombineering)

 
## Case Study: Recombineering Library Experiment
The goal of this case study is to show the reader a real-world usage scenario of the reactor system. Furthermore, it emphasizes the advantage of a fully automated and self-regulating experiment setup.

### Experiment Setup



<img src="doc/case_study.svg" alt="Reactor Configuration"/>

<img src="doc/case_study_sim.jpg" alt="Growth Simulation"/>

### Result
 
<img src="doc/case_study_result.svg" alt="Plate Result"/>


## Software Model

### General

### Phage HW Model #1: Yeast Assembly
...
### Phage HW Model #2: Recombineering
...

## Hardware Reactor


### Hardware Overview
<img src="doc/hardware_overview.svg" alt="Reactor Hardware Overview"/>

### Hardware Components

#### Computer: Raspberry Pi 3B+
<img src="doc/raspberry_pi_3b.jpg" alt="Raspberry Pi 3B+" width="200"/>

[Datasheet](hardware/devices/drivers/hw/datasheets/raspberry_pi_3b.pdf)
[Source](https://www.raspberrypi.org/)


#### Water Temperature Sensor: DS18B20
<img src="doc/ds18b20.jpg" alt="DS18B20" width="200"/>

[Datasheet](hardware/devices/drivers/hw/datasheets/DS18B20.pdf)
[Source](https://www.adafruit.com/product/381)



#### Thermoelectric Peltier Element: TEC1-12715
<img src="doc/tec1-12715.jpg" alt="TEC1-12715" width="200"/>

[Datasheet](hardware/devices/drivers/hw/datasheets/TEC1_12715.pdf)
[Source](https://www.aliexpress.com/)


#### Electronic Speed Controller ESC
<img src="doc/ESC.jpg" alt="ESC" width="200"/>

[Datasheet](hardware/devices/drivers/hw/datasheets/ESC.pdf)
[Source](https://www.aliexpress.com/)


#### Microprocessor: Arduino Nano
<img src="doc/arduino_nano.jpg" alt="Arduino Nano" width="200"/>

[Datasheet](hardware/devices/drivers/hw/datasheets/a.pdf)
[Source](https://core-electronics.com.au/)








#### Ambient Temperature and Pressure Sensor: BME280
<img src="doc/bme280.jpg" alt="BME280" width="200"/>

[Datasheet](hardware/devices/drivers/hw/datasheets/BME280.pdf)
[Source](https://learn.adafruit.com/adafruit-bme280-humidity-barometric-pressure-temperature-sensor-breakout)


#### 8 Channel Input/Output Port Extender: PCF8574
<img src="doc/pcf8574.jpg" alt="PCF8574" width="200"/>

[Datasheet](hardware/devices/drivers/hw/datasheets/PCF8574.pdf)
[Source](https://www.aliexpress.com/)


#### Light Emitting Diode LED: TLCY5800
<img src="doc/tlcy5800.jpg" alt="TLCY5800" width="200"/>

[Datasheet](hardware/devices/drivers/hw/datasheets/TLCY5800.pdf)
[Source](https://www.distrelec.ch/de/led-gelb-mm-vishay-tlcy5800/p/30105848)


#### I2C Bus Multiplexer: TCA9548A
<img src="doc/tca9548a.jpg" alt="TCA9548A" width="200"/>

[Datasheet](hardware/devices/drivers/hw/datasheets/TCA9448A.pdf)
[Source](https://learn.adafruit.com/adafruit-tca9548a-1-to-8-i2c-multiplexer-breakout/overview)


#### High Dynamic Range Digital Light Sensor: TSL2591
<img src="doc/tsl2591.jpg" alt="TSL2591" width="200"/>

[Datasheet](hardware/devices/drivers/hw/datasheets/TSL2591.pdf)
[Source](https://www.adafruit.com/product/1980)


#### 16 Channel Pulse Width Modulation Module: PCA9685
<img src="doc/pca9685.jpg" alt="PCA9685" width="200"/>

[Datasheet](hardware/devices/drivers/hw/datasheets/PCA9685.pdf)
[Source](https://www.adafruit.com/product/815)


#### Optocoupler: TLP281
<img src="doc/tlp281.jpg" alt="TLP281" width="200"/>

[Datasheet](hardware/devices/drivers/hw/datasheets/TLP281-4.pdf)
[Source](https://www.aliexpress.com/)


#### Magnetic Stirrer
<img src="doc/magnetic_stirrer.jpg" alt="Magnetic Stirrer" width="200"/>

[Datasheet](hardware/devices/drivers/hw/datasheets/magnetic_stirrer.pdf)
[Source](https://www.aliexpress.com/)


#### CPU PC Fan
<img src="doc/cpu_fan.jpg" alt="CPU PC Fan" width="200"/>

[Datasheet](hardware/devices/drivers/hw/datasheets/cpu_fan.pdf)
[Source](https://www.bequiet.com/en)


#### Water Pump
<img src="doc/water_pump.jpg" alt="Water Pump" width="200"/>

[Datasheet](hardware/devices/drivers/hw/datasheets/water_pump.pdf)
[Source](https://www.aliexpress.com/)


#### Peristaltic Pump
<img src="doc/peristaltic_pump.jpg" alt="Peristaltic Pump" width="200"/>

[Datasheet](hardware/devices/drivers/hw/datasheets/peristaltic_pump.pdf)
[Source](https://www.aliexpress.com/)


#### Mosfet Transistor
<img src="doc/mosfet.jpg" alt="Mosfet Transistor" width="200"/>

[Datasheet](hardware/devices/drivers/hw/datasheets/mosfet.pdf)
[Source](https://www.aliexpress.com/)


#### Control Terminal




### Software Overview
<img src="doc/software_overview.svg" alt="Reactor Software Overview"/>


### Devices
...

####  Online Optical Density Sensor
<img src="doc/od_sensor.svg" alt="Optical Density Sensor"/>
...

##### Calibration
<img src="doc/od_calibration_raw_data.png" alt="Raw Sensor Data"/>
<img src="doc/od_calibration_ref_data.png" alt="Reference Data"/>
<img src="doc/od_calibration_relation.png" alt="Relation Light Sensor and OD"/>
<img src="doc/od_calibration_regression.png" alt="Regression"/>
<img src="doc/od_calibration_sample_run.png" alt="Sample Run"/>


#### Reactor Temperature Control
<img src="doc/temperature_control.svg" alt="Temperature Control"/>

<img src="doc/temperature_control_heating387.png" alt="Reactor Heating"/>
<img src="doc/temperature_control_cooling222.png" alt="Reactor Cooling"/>


...

#### Peristaltic Pump
...


### Drivers
...

### HW
...

#### 1 Wire
...
* DS18B20


#### I2C
...
* BME280
* PCA9685
* PCF8574
* TCA9548A
* TSL2591



## Hardware Software Interaction
...

### Motivation


### Naive Constant Cell Density Controller

### Advanced Naive Constant Cell Density Controller

### Model Driven Constant Cell Density Controller

### Model Driven Constant Cell Denisty Controller with Fluorescent Original Host


## Usage
```
connect to the device:
1. plug in the power cable and switch on the power supply (the system starts up autoatically)
2. connect to the wifi network 'igem-ethz' (you should get an ip address from the DHCP server in the range 192.168.4.2-100)
3. connect to the server at address 192.168.4.1: (i.e. ssh pi@192.168.4.1)
 - username: pi
 - password: PASSWORD
4. change directory to igem19-ethz-phage-hw-model (i.e. cd igem19-ethz-phage-hw-model)
5. start the reactor software using the command: ./startup.sh
6. after the automatic device initialization, you should see all available commands printed to stdout
```

```
Commands
//TODO
```


```
fetch the whole repo:
git clone https://github.com/andreaskuster/igem19-ethz-phage-hw-model.git
```

```
update local repo to the most recent version:
git pull
```

```
keep the experiment running while disconnecting the computer:
- at startup, run: screen
- detach from session: Ctrl + a d
- attach to session: screen -r
```
```
connect to the graphical user interface:
1. connect to the wifi
2. use vnc viewer (realvnc)
 -address: 192.168.4.1
 -username: pi
```

## Raspberry Pi Setup
...

## 3D Print CAD Design

### Optical Density Sensor

### Water Bath

## Cleaning Procedure
* Pipes
    1. Rinse pipes using 70% ethanol
    2. Remove all pipes and autoclave them
    
* OD cuvettes
    1. one-way -> trash

* Reactor Flasks
    1. autoclave
    
 Additionally: do not mix phage-contaminated material with non-contaminated ones.