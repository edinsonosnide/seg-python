import numpy as np

#Se usa para llamar a la funcion que crea las funciones de
#transformacion y llamar a la funcion que realiza la transormacion
#con las funciones lineales halladas
def h_matching(trainData, testData, k):
    funcs = training(trainData, k)
    standardized_data = testing(testData, funcs)
    return standardized_data

#Usando las funciones de transformacion, en el testData se halla el percentil
#de cada voxel para hallar la nueva intensidad de ese voxel segun ese percentil hallado
def testing(testData, functions):

    standardized_data = np.zeros(testData.shape)

    sorted_testData = np.sort(testData.flatten())
    len_sorted_testData = len(sorted_testData)

    for i in range(testData.shape[0]):
        for j in range(testData.shape[1]):
            for k in range(testData.shape[2]):
                index = np.searchsorted(sorted_testData, testData[i,j,k])
                percentile = (index + 1) / len_sorted_testData * 100
                for func in functions:
                    if func['startPercentile'] <= percentile < func['endPercentile']:
                        standardized_data[i, j, k] = func['func'](percentile)

    return standardized_data

#Se crean las funciones con las que se van a transformar el testData (nuevo data)
def training(trainData, k):
    percentiles = np.linspace(0, 100, k) #X
    y = np.percentile(trainData.flatten(), percentiles) #Y
    functions = []

    for i in range(k - 1):
        start = percentiles[i]
        end = percentiles[i + 1]
        m_i = (y[i + 1] - y[i]) / (percentiles[i+1] - percentiles[i])
        b_i = y[i] - m_i * percentiles[i]
        functions.append({'startPercentile': start, 'endPercentile': end, 'func': lambda x, m=m_i, b=b_i: m * x + b})

    return functions



# Ejemplo de uso
myNumberOfK = 5
myTrainData = np.array([
    [
        [14, 24, 13],
        [44, 54, 16],
        [1, 12, 11]
    ]
])
myTestData = np.array([
    [
        [-1, 2, 3],
        [4, 5, 2],
        [6, 2, 1]
    ]
])

def debug():
    myTrainData = np.random.randint(1, 1001, size=(100, 100, 100))
    myTestData = np.random.randint(1, 100, size=(20, 20, 20))

    result = h_matching(myTrainData, myTestData, myNumberOfK)
    print(result)

    import matplotlib.pyplot as plt

    # Graficar el histograma de los datos de entrenamiento
    plt.figure(figsize=(8, 6))
    plt.hist(myTrainData.flatten(), alpha=0.7, edgecolor='black')
    plt.title('Histograma de myTrainData')
    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    plt.grid(True)
    plt.show()

    # Graficar el histograma de los datos de prueba
    plt.figure(figsize=(8, 6))
    plt.hist(myTestData.flatten(), alpha=0.7, edgecolor='black')
    plt.title('Histograma de myTestData')
    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    plt.grid(True)
    plt.show()

    # Graficar el histograma de los datos de prueba
    plt.figure(figsize=(8, 6))
    plt.hist(result.flatten(), alpha=0.7, edgecolor='black')
    plt.title('Histograma de result')
    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    plt.grid(True)
    plt.show()
debug()

