# EE109 Digital System Lab Final Report
Ron Domingo (rdomingo) and Michael Lu (mingci7)

## Table of Contents
- Application Overview
- Software Simulation
- Hardware Implementation
- Design Tradeoffs
- Appendix

## Application Overview
``
Machine Learning is an evolving field that has impacted many sectors of society, enabling new technologies and eliminating costly, manual efforts such as data analysis. One application that requires a costly and tedious process is the colorization of black-and-white photos, which used to require dozens of hours selecting proper color hues and attempting to make color contrasts realistic. With the rise of CNNs, however, computerized colorization trained on neural networks has been shown to achieve up to 32% success rates in fooling humans into believing the image is real. The downside to this automated approach is that CNNs take a lot of time and software resources to train and run. Therefore, it could take hours and even days to train a proposed model and determine the parameters for most accurate prediction. Hardware resources can speed up low-level operations such as convolution and multiply-and-add, which are the main bottleneck of CNN training and inference. We attempt to implement the colorization CNN in hardware, checking to see if deploying the CNN on hardware could result in multiple folds in speedup.
(Links to the CNN framework and model we based our implementation on:
Paper: https://arxiv.org/pdf/1603.08511.pdf
GitHub repo: https://github.com/richzhang/colorization)
![system_diagram](./img/colorization_CNN_model.png)
``

## Software Simulation 
```
// Add an overview of your software simulation here.
// If you have references to some urls, you can add the them like this: 
// [this is a link to a webpage](https://en.wikipedia.org/wiki/Sobel_operator)
```

## Hardware Implementation
![system_diagram](./img/hardware_design.png)
```
// Add an overview of your haredware implementation here.
// If you want to attach an image of your system diagram, you can leave the image in the 
// img folder, and add it like this: 
// ![system_diagram](./img/system_diagram.jpg)

```

## Design Tradeoffs
```
// Discuss your tradeoffs between the design choices you've made
```

## Appendix
```
// If you have any comments about the class, or have a video you want to show us, 
// feel free to add them in the Appendix.
```
