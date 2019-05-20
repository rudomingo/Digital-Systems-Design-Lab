import numpy as np
import csv

def convolve(inputs, filters, bias, stride=1):
    '''
        Caffe implementation of convolution as well as the ReLU layer.

        Info can be found here:
            https://github.com/Yangqing/caffe/wiki/Convolution-in-Caffe:-a-memo
    '''

    input_dims = inputs.shape
    depth = input_dims[0]
    width = input_dims[1]
    height = input_dims[2]
    filters_dims = filters.shape
    num_filters = filters_dims[0]
    kernel_size = filters_dims[1]

    output = np.zeros((width/stride, height/stride, depth))
    for w in range(0, width, stride):
        for h in range(0, height, stride):
            for x in range(kernel_size):
                for y in range(kernel_size):
                    for m in range(num_filters):
                        # Sets each starting value to be the bias
                        output[w, h, m] = bias[m]
                        for d in range(depth):
                            if (w < kernel_size or h < kernel_size):
                                output[w, h, m] += 0;
                            else:
                                output[w, h, m] += inputs[w+x, h+y, d] * filters[m, x, y, d]
                        if output[w, h, m] < 0:
                                output[w, h, m] = 0
    return output

def normalization(inputs, mean, variance):
    input_dims = inputs.shape
    depth = input_dims[0]
    width = input_dims[1]
    height = input_dims[2]

    output = np.zeros((width, height, depth))
    for w in range(width):
        for h in range(height):
            for d in range(depth):
                output[w, h, d] = (input[w, h, d] - mean[d])/variance[d]
    return output            

if __name__ == '__main__':
    print("Hello, world!")

def read_csv(fileName):
    weights = []
    with open(fileName, 'rb') as csvfile:
        weights_reader = csv.reader(csvfile, delimiter=',')
        for row in weights_reader:
            weights.append(row)
    return weights


# Importing weights and biases for all layers
weights1_1 = read_csv('XXXXX.csv')
bias1_1 = read_csv('XXXXX.csv')
weights1_2 = read_csv('XXXXX.csv')
bias1_2 = read_csv('XXXXX.csv')
mean_1 = read_csv('XXXXX.csv')
variance_1 = read_csv('XXXXX.csv')

weights2_1 = read_csv('XXXXX.csv')
bias2_1 = read_csv('XXXXX.csv')
weights2_2 = read_csv('XXXXX.csv')
bias2_2 = read_csv('XXXXX.csv')
mean_2 = read_csv('XXXXX.csv')
variance_2 = read_csv('XXXXX.csv')

weights3_1 = read_csv('XXXXX.csv')
bias3_1 = read_csv('XXXXX.csv')
weights3_2 = read_csv('XXXXX.csv')
bias3_2 = read_csv('XXXXX.csv')
weights3_3 = read_csv('XXXXX.csv')
bias3_3 = read_csv('XXXXX.csv')
mean_3 = read_csv('XXXXX.csv')
variance_3 = read_csv('XXXXX.csv')

weights4_1 = read_csv('XXXXX.csv')
bias4_1 = read_csv('XXXXX.csv')
weights4_2 = read_csv('XXXXX.csv')
bias4_2 = read_csv('XXXXX.csv')
weights4_3 = read_csv('XXXXX.csv')
bias4_3 = read_csv('XXXXX.csv')
mean_4 = read_csv('XXXXX.csv')
variance_4 = read_csv('XXXXX.csv')

weights5_1 = read_csv('XXXXX.csv')
bias5_1 = read_csv('XXXXX.csv')
weights5_2 = read_csv('XXXXX.csv')
bias5_2 = read_csv('XXXXX.csv')
weights5_3 = read_csv('XXXXX.csv')
bias5_3 = read_csv('XXXXX.csv')
mean_5 = read_csv('XXXXX.csv')
variance_5 = read_csv('XXXXX.csv')

weights6_1 = read_csv('XXXXX.csv')
bias6_1 = read_csv('XXXXX.csv')
weights6_2 = read_csv('XXXXX.csv')
bias6_2 = read_csv('XXXXX.csv')
weights6_3 = read_csv('XXXXX.csv')
bias6_3 = read_csv('XXXXX.csv')
mean_6 = read_csv('XXXXX.csv')
variance_6 = read_csv('XXXXX.csv')

weights7_1 = read_csv('XXXXX.csv')
bias7_1 = read_csv('XXXXX.csv')
weights7_2 = read_csv('XXXXX.csv')
bias7_2 = read_csv('XXXXX.csv')
weights7_3 = read_csv('XXXXX.csv')
bias7_3 = read_csv('XXXXX.csv')
mean_7 = read_csv('XXXXX.csv')
variance_7 = read_csv('XXXXX.csv')

weights8_1 = read_csv('XXXXX.csv')
bias8_1 = read_csv('XXXXX.csv')
weights8_2 = read_csv('XXXXX.csv')
bias8_2 = read_csv('XXXXX.csv')
weights8_3 = read_csv('XXXXX.csv')
bias8_3 = read_csv('XXXXX.csv')
mean_8 = read_csv('XXXXX.csv')
variance_8 = read_csv('XXXXX.csv')

# Padding of 1 involved in most of the convolutions, as well as dilation factors for some
# Might need to include for more accurate results
test_image = read_csv('XXXXX.csv')
layer1_1 = convolve(test_image, weights1_1, bias1_1)
layer1_2 = convolve(layer1_1, weights1_2, bias1_2, 2)
normalized_1 = normalization(layer1_2, mean_1, variance_1)

layer2_1 = convolve(normalized_1, weights2_1, bias2_1)
layer2_2 = convolve(layer2_1, weights2_2, bias2_2, 2)
normalized_2 = normalization(layer2_2, mean_2, variance_2)

layer3_1 = convolve(normalized_2, weights3_1, bias3_1)
layer3_2 = convolve(layer3_1, weights3_2, bias3_2)
layer3_3 = convolve(layer3_2, weights3_3, bias3_3, 2)
normalized_3 = normalization(layer3_3, mean_3, variance_3)

layer4_1 = convolve(normalized_3, weights4_1, bias4_1)
layer4_2 = convolve(layer4_1, weights4_2, bias4_2)
layer4_3 = convolve(layer4_2, weights4_3, bias4_3)
normalized_4 = normalization(layer4_3, mean_4, variance_4)

layer5_1 = convolve(normalized_4, weights5_1, bias5_1)
layer5_2 = convolve(layer5_1, weights5_2, bias5_2)
layer5_3 = convolve(layer5_2, weights5_3, bias5_3)
normalized_5 = normalization(layer5_3, mean_5, variance_5)

layer6_1 = convolve(normalized_5, weights6_1, bias6_1)
layer6_2 = convolve(layer6_1, weights6_2, bias6_2)
layer6_3 = convolve(layer6_2, weights6_3, bias6_3)
normalized_6 = normalization(layer6_3, mean_6, variance_6)

layer7_1 = convolve(normalized_7, weights7_1, bias7_1)
layer7_2 = convolve(layer7_1, weights7_2, bias7_2)
layer7_3 = convolve(layer7_2, weights7_3, bias7_3)
normalized_7 = normalization(layer7_3, mean_7, variance_7)

layer8_1 = convolve(normalized_7, weights8_1, bias8_1)
layer8_2 = convolve(layer8_1, weights8_2, bias8_2)
layer8_3 = convolve(layer8_2, weights8_3, bias8_3)
normalized_8 = normalization(layer8_3, mean_8, variance_8)
