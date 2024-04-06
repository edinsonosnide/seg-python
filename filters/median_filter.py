import numpy as np
import math

def median_filter(inputData: np.ndarray) -> np.ndarray:

    #only 4 neighbors for speed - results are not very different with more neighbors
    neighbors = [
        (1, 0, 0), (0, 0, 1), (0, 1, 0),(0, -1, 0)
    ]

    # Create a mask to not edit the original data
    data = np.zeros_like(inputData, dtype=np.uint8)

    for i in range(inputData.shape[0]):
      for j in range(inputData.shape[1]):
        for k in range(inputData.shape[2]):
            intensities = np.array([])
            # get the mean of neighbors
            for dx, dy, dz in neighbors:
                x, y, z = i + dx, j + dy, k + dz
                if (0 <= x < inputData.shape[0] and 0 <= y < inputData.shape[1] and 0 <= z < inputData.shape[2]):
                   intensities = np.append(intensities, [inputData[x][y][z]])
            data[i][j][k] = np.median(intensities)

    return data