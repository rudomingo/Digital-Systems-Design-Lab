import caffe_pb2 as cq
import inspect
import numpy as np

if __name__ == '__main__':
    
    f = open('colorization_release_v2.caffemodel', 'rb')
    cq2 = cq.NetParameter()
    cq2.ParseFromString(f.read())
    f.close()
    for layer in cq2.layer:
        print(layer.name)
    layer = cq2.layer[11]
    data = np.asarray(layer.blobs)
    print(data[0].data)
    #print(inspect.getmembers(layer))

