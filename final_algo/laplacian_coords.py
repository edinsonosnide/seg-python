import numpy as np
def laplacian_coords(inputData: np.ndarray) -> np.ndarray:
    return inputData

def calculate_weights(image, beta=5.0):
    height, width = image.shape
    num_pixels = height * width
    indices = np.arange(num_pixels).reshape(height, width)
    W = np.zeros((num_pixels, num_pixels))

    # Primero encontrar sigma, la máxima diferencia de intensidad entre vecinos
    sigma = 0
    for i in range(height):
        for j in range(width):
            if i > 0:  # Arriba
                sigma = max(sigma, np.abs(image[i, j] - image[i-1, j]))
            if i < height - 1:  # Abajo
                sigma = max(sigma, np.abs(image[i, j] - image[i+1, j]))
            if j > 0:  # Izquierda
                sigma = max(sigma, np.abs(image[i, j] - image[i, j-1]))
            if j < width - 1:  # Derecha
                sigma = max(sigma, np.abs(image[i, j] - image[i, j+1]))

    # Asegurarse de que sigma no sea cero para evitar división por cero
    if sigma == 0:
        sigma = 1

    # Calcular los pesos con el sigma encontrado
    for i in range(height):
        for j in range(width):
            index = indices[i, j]
            if i > 0:  # Arriba
                W[index, indices[i-1, j]] = np.exp(-beta * (np.abs(image[i, j] - image[i-1, j]) / sigma))
            if i < height - 1:  # Abajo
                W[index, indices[i+1, j]] = np.exp(-beta * (np.abs(image[i, j] - image[i+1, j]) / sigma))
            if j > 0:  # Izquierda
                W[index, indices[i, j-1]] = np.exp(-beta * (np.abs(image[i, j] - image[i, j-1]) / sigma))
            if j < width - 1:  # Derecha
                W[index, indices[i, j+1]] = np.exp(-beta * (np.abs(image[i, j] - image[i, j+1]) / sigma))

    return W

def calculate_D_from_W(W):
    # Calcular D como la suma de cada fila de W
    D = np.sum(W, axis=1)
    return D


import scipy.sparse as sp
from scipy.sparse.linalg import spsolve


def laplacian_segmentation(image, seeds, labels, xB=1, xF=0, k1=1, k2=1, k3=1, beta=5.0):
    height, width = image.shape
    num_pixels = height * width
    indices = np.arange(num_pixels).reshape(height, width)

    W = calculate_weights(image, beta)
    D = calculate_D_from_W(W)

    # Construir la matriz Laplaciana L
    L = sp.diags(D) - sp.csr_matrix(W)

    # Construir el vector b para las condiciones de frontera basadas en semillas
    b = np.zeros(num_pixels)
    for seed, label in zip(seeds, labels):
        b[indices[seed]] = xB if label == 'B' else xF

    # Solucionar el sistema lineal
    A = k1 * sp.eye(num_pixels) + k2 * sp.eye(num_pixels) + k3 * L.dot(L)
    x = spsolve(A, b)

    # Asignar etiquetas según la regla especificada
    segmented_image = x.reshape((height, width))
    segmented_image = np.where(segmented_image >= (xB + xF) / 2, xB, xF)

    return segmented_image


import numpy as np


def get_seeds_and_labels(annotations, background_value=0, foreground_value=1):
    height, width = annotations.shape
    seeds = []
    labels = []

    # Recorrer la matriz de anotaciones
    for i in range(height):
        for j in range(width):
            if annotations[i, j] == background_value:
                seeds.append((i, j))  # Añadir la posición como tupla
                labels.append('B')  # 'B' para fondo
            elif annotations[i, j] == foreground_value:
                seeds.append((i, j))
                labels.append('F')  # 'F' para primer plano

    return seeds, labels

# Ejemplo de uso:
# annotations = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])  # Matriz de ejemplo
# seeds, labels = get_seeds_and_labels(annotations)
# print("Seeds:", seeds)
# print("Labels:", labels)


def set_b_vector(seeds, labels, height, width, xB, xF):
    num_pixels = height * width
    b = np.zeros(num_pixels)
    indices = np.arange(num_pixels).reshape(height, width)

    for (i, j), label in zip(seeds, labels):
        index = indices[i, j]
        b[index] = xB if label == 'B' else xF

    return b

# Continuando el ejemplo anterior:
# xB = 1  # Valor para el fondo
# xF = 0  # Valor para el primer plano
# b = set_b_vector(seeds, labels, annotations.shape[0], annotations.shape[1], xB, xF)
# print("Vector b:", b)
import numpy as np

# Suponiendo que L es tu matriz Laplaciana y x es tu vector de valores
def calculate_norm_squared(L, x):
    Lx = np.dot(L, x)  # Aplicar L a x para obtener Lx
    norm_squared = np.dot(Lx, Lx)  # Calcular (Lx)^T * Lx que es la norma cuadrada de Lx
    return norm_squared

# Ejemplo de uso
# L = np.array([[2, -1, 0], [-1, 2, -1], [0, -1, 2]])  # Ejemplo de matriz Laplaciana
# x = np.array([1, 2, 3])  # Vector de ejemplo
# result = calculate_norm_squared(L, x)
# print("Norma cuadrada de Lx:", result)


import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import spsolve, factorized


def segment_image(image, seeds, labels, xB, xF, beta):
    height, width = image.shape
    num_pixels = height * width
    indices = np.arange(num_pixels).reshape(height, width)

    W = calculate_weights(image, beta)
    D = np.sum(W, axis=1)
    L = sp.diags(D) - W
    L2 = L.dot(L)

    # Preparar I_s, donde sólo los elementos de las semillas son 1
    I_s = sp.lil_matrix((num_pixels, num_pixels))
    b = np.zeros(num_pixels)
    for (i, j), label in zip(seeds, labels):
        idx = indices[i, j]
        I_s[idx, idx] = 1
        b[idx] = xB if label == 'B' else xF

    A = I_s + L2
    # Usando factorización Cholesky para resolver el sistema
    A = sp.csr_matrix(A)
    solve = factorized(A)  # Factorización Cholesky
    x = solve(b)

    segmented_image = x.reshape((height, width))
    return segmented_image

# Suponer que se proporcionan image, seeds, labels correctamente.