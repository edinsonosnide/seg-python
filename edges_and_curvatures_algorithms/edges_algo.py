import numpy as np
import scipy
def edges_algo(inputData):

    kernel_x = np.array([-1, 1]) / 2

    Dx = scipy.ndimage.convolve(inputData, kernel_x.reshape((2, 1, 1)))
    Dy = scipy.ndimage.convolve(inputData, kernel_x.reshape((1, 2, 1)))
    Dz = scipy.ndimage.convolve(inputData, kernel_x.reshape((1, 1, 2)))

    data = np.sqrt(Dx ** 2 + Dy ** 2 + Dz ** 2)

    return data