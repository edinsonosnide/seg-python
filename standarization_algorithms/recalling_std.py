import numpy as np

def rescaling_std(inputData: np.ndarray) -> np.ndarray:
    flattengInputData = inputData.flatten()
    minIntensity = np.min(flattengInputData)
    maxIntensity = np.max(flattengInputData)
    print("old minIntensity: ", minIntensity)
    print("old maxIntensity: ", maxIntensity)

    # Rescale the intensities to the range [0, 1]
    data = (inputData - minIntensity) / (maxIntensity - minIntensity)

    flattengData = data.flatten()
    minIntensity = np.min(flattengData)
    maxIntensity = np.max(flattengData)
    print("new minIntensity: ", minIntensity)
    print("new maxIntensity: ", maxIntensity)
    return data