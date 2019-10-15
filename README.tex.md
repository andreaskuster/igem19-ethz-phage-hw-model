# <img src="igem-ethz-logo.svg" alt="iGEM ETHZ Logo" width="75"/> iGEM ETH Zurich - <img src="igem19-ethz-logo.svg" alt="iGEM 19 ETHZ Logo" width="120"/> Libraries for Personalized Phage Therapy

## Abstract
Antibiotic resistant pathogens are a major threat to global health. Emerging superbugs are rapidly becoming resistant to available antibiotics, while the discovery of new antibiotics is falling behind. Phage therapy offers a potential solution that has achieved remarkable successes. However, it is limited by the number of pathogens that can be targeted by available natural phages. To address this limitation, we aim to increase the range of phage specificities. Host specificity is influenced by the affinity of the phage’s binding protein to the bacterial surface. We developed a system that integrates random codons in phage genomes at any locus of interest. This allows for the formation of phage libraries with novel binding proteins that alter the host spectrum. Our bioreactor selects and evolves the best variants. The observed phage-host interactions can be used to further improve library design. Our system could be the basis for personalized treatment of bacterial infections. 
We are currently testing three approaches to generate these libraries.
* Yeast assembly: a plasmid containing the T7 genome is assembled by homologous recombination in yeast and a library of randomized oligos is inserted into variable region of tail fiber protein.
* Recombineering: A randomised sequence present on a plasmid is inserted into the tail fiber gene in vivo by using E. coli's homologous recombination machinery.
* In vitro: The tail fiber variable regions are ligated to the T7 genome in vitro by Gibson assembly. 

## Project Trailer
[![T007 - License to Lyse - iGEM 2019 ETH Zurich - Trailer](https://img.youtube.com/vi/lpeFW6eoZ5g/maxresdefault.jpg)](https://www.youtube.com/watch?v=lpeFW6eoZ5g?autoplay=1)

## Software Model

### General

### Phage HW Model #1: Yeast Assembly
...
### Phage HW Model #2: Recombineering
...

## Hardware Reactor
// TODO: add reactor photo

### Abstract // TODO: add final version
Experiments involving bacterial cell growth are limited by tedious manual tasks such as cell density measurements and growth medium addition. To overcome these issues, we developed a highly customizable, extendable and cost-efficient bioreactor. Independent flasks for cell growth are integrated with temperature control, continuous OD measurement using our self-built OD sensors and peristaltic pumps. 
 
Complementary software allows implementation of new experimental setups, custom control and monitoring mechanisms. Remote access and alerts permit unsupervised, long-term experiments. Collected data from ongoing experiments can be used to determine parameters such as growth rates which in turn can be used to make predictions and adjust growth conditions accordingly. 
Hardware design, software and documentation are freely available.
 
Our prototype was of great use for our long term and large volume experiments which led to multiple iterations of hardware and software improvements.This reactor is a valuable tool that significantly increases efficiency and experiment reproducibility.



### Hardware Overview
<img src="hardware_overview.svg" alt="Reactor Hardware Overview"/>

### Hardware Components
...

### Software Overview
...

### HW
...

#### I2C
...

#### 1 Wire
...

### Drivers
...

### Devices
...

## Hardware Software Interaction
...

### Motivation


### Naive Constant Cell Density Controller

### Model Driven Constant Cell Density Controller


## Usage

```
git clone https://github.com/andreaskuster/igem19-ethz-phage-hw-model.git
cd igem19-ethz-phage-hw-model
./startup.sh
```


```

```