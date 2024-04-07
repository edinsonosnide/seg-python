import numpy as np
import math
def white_stripe_std(inputData: np.ndarray) -> np.ndarray:
    flattenInputData = inputData.flatten()
    minIntensity = np.min(flattenInputData)
    maxIntensity = np.max(flattenInputData)
    print("old minIntensity: ", minIntensity)
    print("old maxIntensity: ", maxIntensity)


    # Obtener el array de intensidades
    intensity_values = inputData.flatten()

    # Calcular el histograma y los bins de intensidades
    hist, bins = np.histogram(intensity_values, bins=50)
    print(hist)
    print("len of hist: ", len(hist))
    # Due that there is one more bin than elements in hist:
    bins = bins[:-1]
    print(bins)
    print("len of bins: ", len(bins))

    all_peaks_bin_value = []

    #append all the peaks to all_peaks
    for i in range(0,len(hist)):
        if i - 1 >= 0 and i + 1 < len(hist):
            if hist[i - 1] < hist[i] and hist[i] > hist[i + 1]:
                print("peak: ", hist[i - 1], hist[i], hist[i+1])
                all_peaks_bin_value.append(bins[i])


    #take the last element
    ws = all_peaks_bin_value[len(all_peaks_bin_value) - 1]
    print("ws: ",all_peaks_bin_value[len(all_peaks_bin_value) - 1])
    # Create a mask to set the result
    data = np.zeros_like(inputData, dtype=float)

    #edit the mask to create the result
    for i in range(inputData.shape[0]):
        for j in range(inputData.shape[1]):
            for k in range(inputData.shape[2]):
                    data[i][j][k] = inputData[i][j][k]/ws

    # Obtener el array de intensidades
    intensity_values = data.flatten()
    flattenData = data.flatten()
    minIntensity = np.min(flattenData)
    maxIntensity = np.max(flattenData)
    print("new minIntensity: ", minIntensity)
    print("new maxIntensity: ", maxIntensity)
    return data