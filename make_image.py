import numpy as np

if __name__ == '__main__':
    image = np.zeros((224, 224))
    #image.fill(1.0)
    np.savetxt("test_image.csv", image, delimiter=',')
    
