import numpy as np
from queue import Queue

def algoRegionGrowing(data: np.ndarray, seeds: list, intensity_input: int):
    # Ensure the data is a valid 3D array
    if len(data.shape) != 3:
        raise ValueError("Input data must be a 3D array")

    # Create a mask to keep track of visited voxels
    mask = np.zeros_like(data, dtype=np.uint8)

    # Define 26-connectivity for region growing in 3D
    '''
    connectivity = [
       (-1, -1, 0),
         (-1, 0, 0),
        (-1, 1, 0),
         (0, -1, 0),
       (0, 0, 0),
        (0, 1, 0),
        (1, -1, 0),
       (1, 0, 0),
        (1, 1, 0),
    ]

    '''
    '''
        connectivity = [
        (-1, -1, -1), (-1, -1, 0), (-1, -1, 1),
        (-1, 0, -1), (-1, 0, 0), (-1, 0, 1),
        (-1, 1, -1), (-1, 1, 0), (-1, 1, 1),
        (0, -1, -1), (0, -1, 0), (0, -1, 1),
        (0, 0, -1), (0, 0, 0), (0, 0, 1),
        (0, 1, -1), (0, 1, 0), (0, 1, 1),
        (1, -1, -1), (1, -1, 0), (1, -1, 1),
        (1, 0, -1), (1, 0, 0), (1, 0, 1),
        (1, 1, -1), (1, 1, 0), (1, 1, 1)
    ]
    '''
    connectivity = [
        (1, 0, 0), (0, 0, 1), (0, 1, 0),(-1, 0, 0), (0, -1, 0),  (0, 0, -1),
    ]





    for seed in seeds:

        intensity_difference = intensity_input #50

        mean_intensity = data[seed[0], seed[1], seed[2]]
        number_of_elements_mean_intensity = 1

        a, b, c = seed
        if mask[a][b][c] == 255:
            continue

        queue = Queue()
        queue.put(seed)

        while not queue.empty():
            x, y, z = queue.get()
            # Check if the voxel is within the data bounds and hasn't been visited
            if (
                0 <= x < data.shape[0] and
                0 <= y < data.shape[1] and
                0 <= z < data.shape[2] and
                mask[x, y, z] == 0
            ):
                # Check the intensity difference with the seed
                if abs(data[x, y, z] - mean_intensity) <= intensity_difference:
                    # Mark the voxel as visited and assign the region label
                    mask[x, y, z] = 255

                    # upadte the mean_intensity
                    number_of_elements_mean_intensity += 1
                    mean_intensity += (mean_intensity - data[x, y, z]) / number_of_elements_mean_intensity

                    # Enqueue neighboring voxels
                    for dx, dy, dz in connectivity:
                        queue.put((x + dx, y + dy, z + dz))
                else:
                    mask[x, y, z] = 127
                    pass
    mask1 = np.zeros_like(mask, dtype=np.uint8)
    mask1[mask == 255] = 255
    return mask1