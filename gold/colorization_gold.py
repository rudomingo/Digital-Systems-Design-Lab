#!/usr/bin/env python

import numpy as np
import multiprocessing as mp
import csv

'''
def convolve(inputs, filters, bias, stride=1, padding_factor=1, dilation=1):

        Caffe implementation of convolution as well as the ReLU layer.

        Info can be found here:
            https://github.com/Yangqing/caffe/wiki/Convolution-in-Caffe:-a-memo

    input_dims = inputs.shape
    depth = input_dims[0]
    width = input_dims[1]
    height = input_dims[2]
    padded_input = pad_matrix(inputs, padding_factor)
    filters_dims = filters.shape
    num_filters = filters_dims[0]
    kernel_size = filters_dims[2]

    if dilation != 1:
        kernel_size = kernel_size + (dilation - 1)*2

    output = np.zeros((num_filters, width/stride, height/stride))

    for w in range(0, width, stride):
        print "current value of w", w
        for h in range(0, height, stride):
            for x in range(kernel_size):
                for y in range(kernel_size):
                    for m in range(num_filters):
                        # Sets each starting value to be the bias
                        output[m, w/stride, h/stride] = bias[m]
                        for d in range(depth):
                            # Output set to zero if not enough of the input matrix is loaded
                            if (w < kernel_size or h < kernel_size):
                                output[m, w/stride, h/stride] += 0;
                            else:
                                if dilation > 1:
                                    # For dilated kernels, convolve only on the non-zero values of the kernel, which depends on the dilation factor
                                    if (x % 2 != 1 or y % 2 != 1):
                                        output[m, w/stride, h/stride] += padded_input[d, w + x/dilation, h + y/dilation] * filters[m, d, x/dilation, y/dilation]
                                else:
                                    # For nondilated kernels, convolve for all values
                                    output[m, w/stride, h/stride] += padded_input[d, w+x, h+y] * filters[m, d, x, y]
                        if output[m, w/stride, h/stride] < 0:
                                output[m, w/stride, h/stride] = 0
    return output
'''
def convolve(inputs, filters, bias, stride=1, padding_factor=1, dilation=1):
    '''
        Caffe implementation of convolution as well as the ReLU layer.

        Info can be found here:
            https://github.com/Yangqing/caffe/wiki/Convolution-in-Caffe:-a-memo
    '''
    input_dims = inputs.shape
    depth = input_dims[0]
    width = input_dims[1]
    height = input_dims[2]
    padded_input = pad_matrix(inputs, padding_factor)
    filters_dims = filters.shape
    num_filters = filters_dims[0]
    kernel_size = filters_dims[2]

    if dilation != 1:
        kernel_size = kernel_size + (dilation - 1)*2

    output = np.zeros((num_filters, width/stride, height/stride))

    # Initialize pool for multiprocessing
    pool = mp.Pool(mp.cpu_count())

    
    # Spawn different processes from the pool to run on different kernels 
    results = [pool.apply_async(miniconvolve, args=(i, padded_input, bias[i], filters[i], depth, width, height, padding_factor, kernel_size, stride, dilation)) for i in range(num_filters)]

    
    for r in results:
        r.wait()
        output[r.get()[0], :, :] = r.get()[1]

    '''
    for i in range(num_filters):
        print "This is the filter number:", i
        single_output = pool.apply(miniconvolve, args=(i, padded_input, bias[i], filters[i], depth, width, height, padding_factor, kernel_size, stride, dilation))
        output[i, :, :] = single_output
    '''
    
    # Close pool
    pool.close()
    
    # Join processes
    pool.join()

    
    # print "This is the output shape: ", output.shape

    return output

def miniconvolve(index, inputs, bias, filters, depth, width, height, padding_factor, kernel_size, stride, dilation):

    output = np.zeros((width/stride, height/stride))
    for w in range(0, width, stride):
        for h in range(0, height, stride):
            for x in range(kernel_size):
                for y in range(kernel_size):
                    # Sets each starting value to be the bias
                    output[w/stride, h/stride] = 0
                    for d in range(depth):
                        # Output set to zero if not enough of the input matrix is loaded
                        if (w < kernel_size or h < kernel_size):
                            output[w/stride, h/stride] += 0;
                        else:
                            if dilation > 1:
                            # For dilated kernels, convolve only on the non-zero values of the kernel, which depends on the dilation factor
                                if (x % 2 != 1 or y % 2 != 1):
                                    output[w/stride, h/stride] += inputs[d, w + x/dilation, h + y/dilation] * filters[d, x/dilation, y/dilation]
                            else:
                                # For nondilated kernels, convolve for all values
                                output[w/stride, h/stride] += inputs[d, w+x, h+y] * filters[d, x, y]
                            output[w/stride, h/stride] += float(bias)
                    if output[w/stride, h/stride] < 0:
                        output[w/stride, h/stride] = 0
    return (index, output)
    # return output


def reshape(inputs):
    input_dims = inputs.shape
    depth = input_dims[0]
    width = input_dims[1]
    height = input_dims[2]

    output = np.zeros((depth*width, height))
    for d in range(depth):
        for w in range(width):
            output[d*width + w] = inputs[d][w] 
    return output

def scale(inputs, factor):
    input_dims = inputs.shape
    depth = input_dims[0]
    width = input_dims[1]
    height = input_dims[2]

    output = np.zeros((depth, width, height))
    for w in range(width):
        for h in range(height):
            for d in range(depth):
                output[d, w, h] = inputs[d, w, h] * factor
    return output

def softmax(inputs):
    input_dims = inputs.shape
    depth = input_dims[0]
    width - input_dims[1]
    height = input_dims[2]

    output = np.zeros((depth, width, height))
    max_val = np.amax(inputs)
    exp_sum = 0
    for w in range(width):
        for h in range(height):
            for d in range(depth):
                inputs[d, w, h] = exp(inputs[d, w, h] - max_val)
                exp_sum += inputs[d, w, h]
    
    for w in range(width):
        for h in range(height):
            for d in range(depth):
                output[d, w, h] = inputs[d, w, h] / exp_sum
    
    return output

def normalization(inputs, mean, variance):
    input_dims = inputs.shape
    depth = input_dims[0]
    width = input_dims[1]
    height = input_dims[2]
    
    output = np.zeros((depth, width, height))
    for w in range(width):
        for h in range(height):
            for d in range(depth):
                # output[d, w, h] = np.subtract(inputs[d, w, h], mean[d]) / variance[d]
                output[d, w, h] = '{:.5f}'.format((float(inputs[d, w, h]) - float(mean[d]))/ float(variance[d]))
    return output

def read_image(fileName, wh):
    image = []
    with open(fileName, 'rb') as csvfile:
        image_reader = csv.reader(csvfile, delimiter=',')
        for row in image_reader:
            image.append(row)
    image = np.asarray(image)
    new_image = image[np.newaxis, ...]
    return new_image

def read_bias(fileName, wh):
    bias = []
    with open(fileName, 'rb') as csvfile:
        bias_reader = csv.reader(csvfile, delimiter=',')
        for row in bias_reader:
            for i in range(len(row)):
                bias.append('{:.5f}'.format(float(row[i])))
    bias = np.asarray(bias)
    return bias.flatten()

def read_weights(fileName, filters, depth, kernel_height, kernel_width):
    weights = [] 
    with open(fileName, 'rb') as csvfile:
        weights_reader = csv.reader(csvfile, delimiter=',')
        for row in weights_reader:
            for i in range(len(row)):
                weights.append('{:.5f}'.format(float(row[i])))
    weights = np.asarray(weights)
    output = np.zeros((filters, depth, kernel_height, kernel_width))
    for f in range(filters):
        for d in range(depth):
            for h in range(kernel_height):
                for w in range(kernel_width):
                    output[f, d, h, w] = weights[f * (depth * kernel_height * kernel_width) + d * (kernel_height * kernel_width) + h * kernel_width + w]
    return output

def read_mean(fileName):
    mean = []
    with open(fileName, 'rb') as csvfile:
        mean_var_reader = csv.reader(csvfile, delimiter=',')
        for row in mean_var_reader:
            mean.append('{:.5f}'.format(float(row[0])))
    mean =  np.asarray(mean)
    return mean.flatten()
    
def read_var(fileName):
    var = []
    with open(fileName, 'rb') as csvfile:
        mean_var_reader = csv.reader(csvfile, delimiter=',')
        for row in mean_var_reader:
            var.append('{:.5f}'.format(float(row[1])))
    var = np.asarray(var)
    return var.flatten()

def pad_matrix(input_matrix, padding_factor):
    input_dims = input_matrix.shape
    depth = input_dims[0]
    width = input_dims[1]
    height = input_dims[2]

    output = np.zeros((depth, width + padding_factor*2, height + padding_factor*2))
    for d in range(depth):
        for w in range(width + padding_factor*2):
            for h in range(height + padding_factor*2):
                if (w < padding_factor or h < padding_factor or h > (height + padding_factor - 1) or w > (width + padding_factor - 1)):
                    output[d, w, h] = 0
                else:
                    output[d, w, h] = input_matrix[d, w - padding_factor, h - padding_factor]
    return output

if __name__ == '__main__':
    print("Hello, world!")


    # Importing weights and biases for all layers
    weights1_1 = read_weights('bw_conv1_1_weights.csv', 64, 1, 3, 3)
    bias1_1 = read_bias('bw_conv1_1_bias.csv', 64)
    weights1_2 = read_weights('conv1_2_weights.csv', 64, 64, 3, 3)
    bias1_2 = read_bias('conv1_2_bias.csv', 64)
    mean_1 = read_mean('conv1_2norm_mean_variance.csv')
    variance_1 = read_var('conv1_2norm_mean_variance.csv')
    '''
    weights2_1 = read_weights('XXXXX.csv', 128, 64, 3, 3)
    bias2_1 = read_bias('XXXXX.csv', 128)
    weights2_2 = read_weights('XXXXX.csv', 128, 128, 3, 3)
    bias2_2 = read_bias('XXXXX.csv', 128)
    mean_2 = read_mean('XXXXX.csv', 128)
    variance_2 = read_var('XXXXX.csv', 128)

    weights3_1 = read_weights('XXXXX.csv', 256, 128, 3, 3)
    bias3_1 = read_bias('XXXXX.csv', 256)
    weights3_2 = read_weights('XXXXX.csv', 256, 256, 3, 3)
    bias3_2 = read_bias('XXXXX.csv', 256)
    weights3_3 = read_weights('XXXXX.csv', 256, 256, 3, 3)
    bias3_3 = read_bias('XXXXX.csv', 256)
    mean_3 = read_mean('XXXXX.csv', 256)
    variance_3 = read_var('XXXXX.csv', 256)

    weights4_1 = read_weights('XXXXX.csv', 512, 256, 3, 3)
    bias4_1 = read_bias('XXXXX.csv', 512)
    weights4_2 = read_weights('XXXXX.csv', 512, 512, 3, 3)
    bias4_2 = read_bias('XXXXX.csv', 512)
    weights4_3 = read_weights('XXXXX.csv', 512, 512, 3, 3)
    bias4_3 = read_bias('XXXXX.csv', 512)
    mean_4 = read_mean('XXXXX.csv', 512)
    variance_4 = read_var('XXXXX.csv', 512)

    weights5_1 = read_weights('XXXXX.csv', 512, 512, 3, 3)
    bias5_1 = read_bias('XXXXX.csv', 512)
    weights5_2 = read_weights('XXXXX.csv', 512, 512, 3, 3)
    bias5_2 = read_bias('XXXXX.csv', 512)
    weights5_3 = read_weights('XXXXX.csv', 512, 512, 3, 3)
    bias5_3 = read_bias('XXXXX.csv', 512)
    mean_5 = read_mean('XXXXX.csv', 512)
    variance_5 = read_var('XXXXX.csv', 512)

    weights6_1 = read_weights('XXXXX.csv', 512, 512, 3, 3)
    bias6_1 = read_bias('XXXXX.csv', 512)
    weights6_2 = read_weights('XXXXX.csv', 512, 512, 3, 3)
    bias6_2 = read_bias('XXXXX.csv', 512)
    weights6_3 = read_weights('XXXXX.csv', 512, 512, 3, 3)
    bias6_3 = read_bias('XXXXX.csv', 512)
    mean_6 = read_mean('XXXXX.csv', 512)
    variance_6 = read_var('XXXXX.csv', 512)

    weights7_1 = read_weights('XXXXX.csv', 512, 512, 3, 3)
    bias7_1 = read_bias('XXXXX.csv', 512)
    weights7_2 = read_weights('XXXXX.csv', 512, 512, 3, 3)
    bias7_2 = read_bias('XXXXX.csv', 512)
    weights7_3 = read_weights('XXXXX.csv', 512, 512, 3, 3)
    bias7_3 = read_bias('XXXXX.csv', 512)
    mean_7 = read_mean('XXXXX.csv', 512)
    variance_7 = read_var('XXXXX.csv', 512)

    weights8_1 = read_weights('XXXXX.csv', 512, 256, 4, 4)
    bias8_1 = read_bias('XXXXX.csv', 512)
    weights8_2 = read_weights('XXXXX.csv', 256, 256, 3, 3)
    bias8_2 = read_bias('XXXXX.csv', 256)
    weights8_3 = read_weights('XXXXX.csv', 256, 256, 3, 3)
    bias8_3 = read_bias('XXXXX.csv', 256)
    mean_8 = read_mean('XXXXX.csv', 256)
    variance_8 = read_var('XXXXX.csv', 256)

    weights8_soft = read_weights('XXXXX.csv', 313, 256, 1, 1)
    bias8_soft = read_bias('XXXXX.csv', 313)
    scale8_param = 2.606
    '''
    # ---------- Beginning of actual CNN -----------------------
   
    test_image = read_image('random_array.csv', 224)
    layer1_1 = convolve(test_image, weights1_1, bias1_1)
    print('Done with first block of first layer')
    print(layer1_1.shape)
    
    layer1_2 = convolve(layer1_1, weights1_2, bias1_2, 2)
    print('Done with second block of first layer')
    print(layer1_2.shape)

    layer1_2_2D = reshape(layer1_2)
    print(layer1_2_2D.shape)
    np.savetxt('first_block_output.csv', layer1_2_2D, delimiter=',')

    '''
    normalized_1 = normalization(layer1_2, mean_1, variance_1)

    print(normalized_1.shape)
    print(normalized_1)
    '''
    '''
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

    layer5_1 = convolve(normalized_4, weights5_1, bias5_1, 1, 2, 2)
    layer5_2 = convolve(layer5_1, weights5_2, bias5_2, 1, 2, 2)
    layer5_3 = convolve(layer5_2, weights5_3, bias5_3, 1, 2, 2)
    normalized_5 = normalization(layer5_3, mean_5, variance_5)

    layer6_1 = convolve(normalized_5, weights6_1, bias6_1, 1, 2, 2)
    layer6_2 = convolve(layer6_1, weights6_2, bias6_2, 1, 2, 2)
    layer6_3 = convolve(layer6_2, weights6_3, bias6_3, 1, 2, 2)
    normalized_6 = normalization(layer6_3, mean_6, variance_6)

    layer7_1 = convolve(normalized_7, weights7_1, bias7_1)
    layer7_2 = convolve(layer7_1, weights7_2, bias7_2)
    layer7_3 = convolve(layer7_2, weights7_3, bias7_3)
    normalized_7 = normalization(layer7_3, mean_7, variance_7)

    layer8_1 = convolve(normalized_7, weights8_1, bias8_1, 2)
    layer8_2 = convolve(layer8_1, weights8_2, bias8_2)
    layer8_3 = convolve(layer8_2, weights8_3, bias8_3)

    # Softmax layer
    layer8_soft_convolve = convolve(layer8_3, weights8_soft, bias8_soft)
    layer8_soft_scaled = scale(layer8_soft_convolve, scale8_param)
    layer8_soft_result = softmax(layer8_soft_scaled)
    '''
