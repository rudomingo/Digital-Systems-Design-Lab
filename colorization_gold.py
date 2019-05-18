import numpy as np

def convolve(inputs, filters, stride=1):
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
                        for d in range(depth):
                            if (w < kernel_size or h < kernel_size):
                                output[w, h, m] += 0;
                            else:
                                output[w, h, m] += inputs[w+x, h+y, d] * filters[m, x, y, d]
                        if output[w, h, m] < 0:
                                output[w, h, m] = 0

    return output

if __name__ == '__main__':
    print("Hello, world!")
