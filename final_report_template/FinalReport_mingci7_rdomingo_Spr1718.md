# EE109 Digital System Lab Final Report
Ron Domingo (rdomingo) and Michael Lu (mingci7)

## Table of Contents
- Application Overview
- Software Simulation
- Hardware Implementation
- Design Tradeoffs
- Appendix

## Application Overview
Machine Learning is an evolving field that has impacted many sectors of society, enabling new technologies and eliminating costly, manual efforts such as data analysis. One application that requires a costly and tedious process is the colorization of black-and-white photos, which used to require dozens of hours selecting proper color hues and attempting to make color contrasts realistic. With the rise of CNNs, however, computerized colorization trained on neural networks has been shown to achieve up to 32% success rates in fooling humans into believing the image is real. The downside to this automated approach is that CNNs take a lot of time and software resources to train and run. Therefore, it could take hours and even days to train a proposed model and determine the parameters for most accurate prediction. Hardware resources can speed up low-level operations such as convolution and multiply-and-add, which are the main bottleneck of CNN training and inference. We attempt to implement the colorization CNN in hardware, checking to see if deploying the CNN on hardware could result in multiple folds in speedup.

(Links to the CNN framework and model we based our implementation on--
Paper: https://arxiv.org/pdf/1603.08511.pdf
GitHub repo: https://github.com/richzhang/colorization)

![system_diagram](./img/colorization_CNN_model.png)

The existing software implementation presented in the GitHub repo runs on an outdated version of Caffe, which is itself outdated and has since been replaced by more advanced and user-friendly deep learning frameworks such as PyTorch and TensorFlow. Additionally, the implementation relied on multiprocessing resources such as GPU acceleration to run training and inference. Even then, it took a long time to train, with some people reporting training times of over a day. We attempted to design a software implementation that would be more accessible for inference purposes, running only on the CPU without extensive use of GPU resources. 

## Software Simulation 
Our software implementation runs the entire CNN on Python, using NumPy as the backbone to creating arrays and running matrix operations. A large roadblock in the process was extracting the weights, bias, mean and variance values from the trained model in Caffe, which required some clever tricks to open up the files, examine the numbers, and then export them to csv files for more convenient matrix conversion. Another issue we encountered was typecasting and converting between 2-D and 4-D arrays, since the weight matrixes were in 4-D but the csv files could only save values in 2-D. Finally, we needed to truncate the 64-bit floating point values to floating point values with five digits after the decimal point to reduce runtime and make sure our implementation could run within a reasonable time period. To that effect, we also introduced a processor pool to run each of the filters for the different convolutional blocks to increase parallelization. 

Our final implementation basically replicated the entire framework of the CNN introduced in the paper and in the GitHub repo, including padding and dilation for the convolutions, normalization after each convolutional layer, and a final softmax layer. Future improvements are always still viable, including rewriting certain parts with GPU code and CUDA acceleration, rewriting the implementation in a lower-level language with SIMD capabilities such as C++ for increased speedup, and further parallelization optimizations.

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
