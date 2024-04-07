import numpy as np
import math
def z_score_std(inputData: np.ndarray) -> np.ndarray:
    flattenInputData = inputData.flatten()
    #flattenInputData = list(set(flattenInputData))
    # Supongamos que "mi_array" es un array
    mi_array = flattenInputData
    # 1. Calcular la media
    media = sum(mi_array) / len(mi_array)
    # 2. Restar la media y elevar al cuadrado
    diferencias_cuadrado = [(x - media) ** 2 for x in mi_array]
    # 3. Calcular la media de las diferencias al cuadrado
    media_diferencias_cuadrado = sum(diferencias_cuadrado) / len(mi_array)
    # 5. Tomar la raíz cuadrada de la media de las diferencias al cuadrado
    desviacion_estandar = math.sqrt(media_diferencias_cuadrado)

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
                data[i][j][k] = (inputData[i][j][k]-media)/desviacion_estandar

    flattengData = data.flatten()
    minIntensity = np.min(flattengData)
    maxIntensity = np.max(flattengData)
    print("new minIntensity: ", minIntensity)
    print("new maxIntensity: ", maxIntensity)
    return data