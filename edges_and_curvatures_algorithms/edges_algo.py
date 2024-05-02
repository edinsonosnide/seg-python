import numpy as np
import spicy
def edges_algo(inputData):

    kernel_x = np.array([[0, 0, 0], [-1, 0, 1], [0, 0, 0]]) / 2
    kernel_y = np.array([[0, -1, 0], [0, 0, 0], [0, 1, 0]]) / 2

    data = np.zeros(inputData.shape)

    #con cualquiera de los tres da el mismo resultado
    for i in range(inputData.shape[0]):
        data[i, :, :] = np.sqrt(spicy.ndimage.convolve(inputData[i, :, :], kernel_x)** 2 +
                                spicy.ndimage.convolve(inputData[i, :, :], kernel_y)** 2)
    #for j in range(inputData.shape[1]):
    #    data[:, j, :] = np.sqrt(spicy.ndimage.convolve(inputData[:, j, :], kernel_x)** 2 +
    #                            spicy.ndimage.convolve(inputData[:, j, :], kernel_y)** 2)
    #for k in range(inputData.shape[2]):
    #    data[:, :, k] = np.sqrt(spicy.ndimage.convolve(inputData[:, :, k], kernel_x)** 2 +
    #                            spicy.ndimage.convolve(inputData[:, :, k], kernel_y)** 2)


    return data