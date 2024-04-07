import numpy as np
import matplotlib.pyplot as plt
def rescaling_std(inputData: np.ndarray) -> np.ndarray:
    flattenInputData = inputData.flatten()
    minIntensity = np.min(flattenInputData)
    maxIntensity = np.max(flattenInputData)
    print("old minIntensity: ", minIntensity)
    print("old maxIntensity: ", maxIntensity)

    # Create a mask
    data = np.zeros_like(inputData, dtype=float)

    for i in range(inputData.shape[0]):
        for j in range(inputData.shape[1]):
            for k in range(inputData.shape[2]):
                data[i][j][k] = (inputData[i][j][k]-minIntensity)/(maxIntensity - minIntensity)


    flattengData = data.flatten()
    minIntensity = np.min(flattengData)
    maxIntensity = np.max(flattengData)
    print("new minIntensity: ", minIntensity)
    print("new maxIntensity: ", maxIntensity)
    print(data.flatten())
    return data