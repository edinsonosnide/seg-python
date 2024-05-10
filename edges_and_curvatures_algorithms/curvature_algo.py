import scipy
import numpy as np
def curvature_algo(inputData):

    kernel_x = np.array([-1, 1]) / 2

    Dx = scipy.ndimage.convolve(inputData, kernel_x.reshape((2, 1, 1)))
    Dxx = scipy.ndimage.convolve(Dx, kernel_x.reshape((2, 1, 1)))
    Dy = scipy.ndimage.convolve(inputData, kernel_x.reshape((1, 2, 1)))
    Dyy = scipy.ndimage.convolve(Dy, kernel_x.reshape((1, 2, 1)))
    Dz = scipy.ndimage.convolve(inputData, kernel_x.reshape((1, 1, 2)))
    Dzz = scipy.ndimage.convolve(Dz, kernel_x.reshape((1, 1, 2)))

    data = np.sqrt(Dxx ** 2 + Dyy ** 2 + Dzz ** 2)

    return data