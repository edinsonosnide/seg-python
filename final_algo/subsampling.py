import numpy as np
def subsampling(inputData: np.ndarray) -> np.ndarray:
    factor = 5
    print(inputData.shape)
    newData = inputData[::factor, ::factor, ::factor]
    print(newData.shape)
    # Obtiene las dimensiones actuales del array
    depth, height, width = newData.shape
    max_dim = max(depth, height, width)

    # Calcula la cantidad de padding necesaria para cada dimensión
    pad_depth = (max_dim - depth)
    pad_height = (max_dim - height)
    pad_width = (max_dim - width)

    # Aplica el padding de ceros al array
    padded_data = np.pad(newData, 
                         ((0, pad_depth), (0, pad_height), (0, pad_width)), 
                         mode='constant', constant_values=0)

    return padded_data
