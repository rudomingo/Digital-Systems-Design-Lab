import caffe_pb2 as cq
import inspect
import numpy as np

if __name__ == '__main__':
    
    # Open the model
    f = open('colorization_release_v2.caffemodel', 'rb')
    model = cq.NetParameter()
    model.ParseFromString(f.read())
    f.close()

    # Loop through the layers of the CNN
    for layer in model.layer:
        print(layer.name)
        # Get the weights from the convolution and norm layers only
        if 'conv' in layer.name:
            if 'norm' in layer.name:
                filename = "{}_mean_variance.csv".format(layer.name)
                # Norm layer format: (0) mean, (1) variance, (2) moving average factor
                blobs = layer.blobs
                mean = np.asarray(blobs[0].data)
                variance = np.asarray(blobs[1].data)
                # Write the mean and variance to a file with the first column as mean
                # and the second column as variance for each line
                csv = np.column_stack((mean, variance))
                np.savetxt(filename, csv, delimiter=',')
            else:
                # Conv layer format: (0) weights, (1) biases
                blobs = layer.blobs
                # Extract the weights and place them in their proper shape
                weights_shape = blobs[0].shape.dim
                print(weights_shape)
                # Reshape the weights to our desired indexing, reducing the shape of the 
                # weights from 4 dims to 2 dims so that it can be placed in a csv file
                weights = np.asarray(blobs[0].data).reshape(weights_shape)
                weights = weights.reshape(weights_shape[0], weights_shape[1]*weights_shape[2]*weights_shape[3])
                filename = "{}_weights.csv".format(layer.name)
                np.savetxt(filename, weights, delimiter=',')
                # Extract the biases for the layer
                biases = np.asarray(blobs[1].data)
                filename = "{}_bias.csv".format(layer.name)
                np.savetxt(filename, biases, delimiter=',')
