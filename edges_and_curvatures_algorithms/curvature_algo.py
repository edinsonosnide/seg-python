import spicy
import numpy as np
def curvature_algo(inputData):
    kernel_x = np.array([[0, 0, 0], [-1, 0, 1], [0, 0, 0]]) / 2
    kernel_y = np.array([[0, -1, 0], [0, 0, 0], [0, 1, 0]]) / 2

    data = np.zeros(inputData.shape)

    # con cualquiera de los tres da el mismo resultado
    for i in range(inputData.shape[0]):
        Dx = spicy.ndimage.convolve(inputData[i, :, :], kernel_x)
        Dxx = spicy.ndimage.convolve(Dx, kernel_x)
        Dxy = spicy.ndimage.convolve(Dx, kernel_y)
        Dy = spicy.ndimage.convolve(inputData[i, :, :], kernel_y)
        Dyy = spicy.ndimage.convolve(Dy, kernel_y)

        data[i, :, :] = np.sqrt(Dxx**2 + Dyy**2)

    #for j in range(inputData.shape[1]):
    #    Dx = spicy.ndimage.convolve(inputData[:, j, :], kernel_x)
    #    Dxx = spicy.ndimage.convolve(Dx, kernel_x)
    #    Dxy = spicy.ndimage.convolve(Dx, kernel_y)
    #    Dy = spicy.ndimage.convolve(inputData[:, j, :], kernel_y)
    #    Dyy = spicy.ndimage.convolve(Dy, kernel_y)

    #    data[:, j, :] = np.sqrt(Dxx**2 + Dyy**2)

    #for k in range(inputData.shape[2]):
    #    Dx = spicy.ndimage.convolve(inputData[:, :, k], kernel_x)
    #    Dxx = spicy.ndimage.convolve(Dx, kernel_x)
    #    Dxy = spicy.ndimage.convolve(Dx, kernel_y)
    #    Dy = spicy.ndimage.convolve(inputData[:, :, k], kernel_y)
    #    Dyy = spicy.ndimage.convolve(Dy, kernel_y)

    #    data[:, :, k] = np.sqrt(Dxx**2 + Dyy**2)

    return data