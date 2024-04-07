import numpy as np
from queue import Queue

def algoRegionGrowing(inputData: np.ndarray, seeds: list, intensity_input: int=50) -> np.ndarray:
    # Ensure the data is a valid 3D array
    if len(inputData.shape) != 3:
        raise ValueError("Input data must be a 3D array")

    # Create a mask to keep track of visited voxels
    mask = np.zeros_like(inputData, dtype=np.uint8)

    # Define 8-connectivity for region growing
    connectivity = [
        (1, 0, 0), (0, 0, 1), (0, 1, 0),(-1, 0, 0), (0, -1, 0),  (0, 0, -1),
    ]

    for seed in seeds:

        intensity_difference = intensity_input

        mean_intensity = inputData[seed[0], seed[1], seed[2]]

        number_of_elements_mean_intensity = 0
        intensities_accumulator = 0

        queue = Queue()
        queue.put(seed)

        while not queue.empty():
            x, y, z = queue.get()
            # Check if the voxel is within the data bounds and hasn't been visited
            if (
                0 <= x < inputData.shape[0] and
                0 <= y < inputData.shape[1] and
                0 <= z < inputData.shape[2] and
                mask[x][y][z] == 0
            ):
                # Check the intensity difference with the seed
                if abs(inputData[x][y][z] - mean_intensity) <= intensity_difference:
                    # Mark the voxel as visited and assign the region label
                    mask[x][y][z] = 255

                    # upadte the mean_intensity
                    number_of_elements_mean_intensity += 1
                    intensities_accumulator += inputData[x, y, z]
                    mean_intensity = intensities_accumulator / number_of_elements_mean_intensity

                    # Enqueue neighboring voxels
                    for dx, dy, dz in connectivity:
                        queue.put((x + dx, y + dy, z + dz))
                else:
                    # this voxel wont take part in the segmentation
                    mask[x][y][z] = 175

    data = np.zeros_like(mask, dtype=np.uint8)
    data[mask == 255] = 255
    return data