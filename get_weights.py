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
                # Norm layer format: (0) mean, (1) variance, (2) moving average factor
                blobs = layer.blobs
                for i in range(len(blobs[0].data)):
                    print("{}\t{}".format(blobs[0].data[i], blobs[1].data[i]))
            else:
                # Conv layer format: (0) weights, (1) biases
                blobs = layer.blobs
                # Extract the weights and place them in their proper shape
                weights = np.asarray(blobs[0].data).reshape(blobs[0].shape.dim)
                print(weights.shape)
                # Extract the biases for the layer
                biases = np.asarray(blobs[1].data)
