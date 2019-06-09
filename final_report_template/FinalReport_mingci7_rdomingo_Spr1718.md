# EE109 Digital System Lab Final Report
Ron Domingo (rdomingo) and Michael Lu (mingci7)

## Table of Contents
- Application Overview
- Software Simulation
- Hardware Implementation
- Design Tradeoffs

## Application Overview
```
// Add an overview of your application here.
```

## Software Simulation 
```
// Add an overview of your software simulation here.
// If you have references to some urls, you can add the them like this: 
// [this is a link to a webpage](https://en.wikipedia.org/wiki/Sobel_operator)
```

## Hardware Implementation
![system_diagram](./img/hardware_design.png)
  Our implementation features two convolution modules that utilize several DRAM elements, and reuse the same set of SRAM elements between the modules. The input, weights, and biases are all saved as csv files that are loaded into DRAM. The weights for the CNN are originally stored in a 4 dimensional matrix, but since csvs are limited to 2 dimensions, the weights were previously flattened to fit the csv format. To account for this, our accelerator has to use a custom indexing scheme to access the proper element in each weights file. In the diagram, the weights and bias DRAM elements have a striped border because they are each not actually one cohesive DRAM element. There are multiple DRAM elements for each of the weights and biases at every convolutional layer. Once the files loaded into DRAM, subsets of the data are loaded into SRAM during the convolution loops. A weights SRAM element was required to buffer the weights data on the FPGA chip because there is not enough SRAM space to store the entire weights data for the different convolution layers. The biases, however, can be loaded completely into SRAM. The line buffer and shift registers are used to buffer the module input in order to perform the convolutions. The output of the convolution is then stored on DRAM also because the outputs would exceed the SRAM space if stored on chip.  
  
  Due to the nature of the convolutions in the colorization CNN, our implementation required two different convolution modules. Convolution 1 in the diagram represents the first image processing convolution where the input has a fixed depth of 1. The Convolution Else features a completely modular convolution function where the depth, channel size, input size, and kernel size are all parameterized. Each of the convolution modules share the same SRAM resources to reduce the memory footprint of the functions. The output of each are also stored in a DRAM buffer so that it can then be read by the next convolution function in the network. 

## Design Tradeoffs
  Our main goal for our accelerator was to reuse as many of the hardware and memory elements as possible. Given the size of the CNN, we knew that an explicit implementation of the network would greatly exceed the resources of the FPGA. Thus we needed to modularize our hardware implementation in order to do the full pipeline. In addition, the weights and function inputs/outputs were too large in size to store in SRAM during the convolutions so we were required to constantly stream data back and forth between DRAM and SRAM so that we can stay within the limitations of the SRAM memory. In doing so we had to incorporate SRAM buffering for many of the DRAM elements. However, a CNN is runs in a linear fashion, so we could reuse the same SRAM elements for each convolution since only one convolution was running at a particular time. This allowed us to reduce our SRAM memory usage for our implementation. Currently, our implementation only performs the first convolutional block of the network which features two convolution layers. However, if were to continue with the project, we would reuse the Convolution Else module defined above and paralellize the convolution loops so that we can greatly maximize the hardware resources of the FPGA. 
