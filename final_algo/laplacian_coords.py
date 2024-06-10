import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import factorized

def laplacian_coords(inputData: np.ndarray,seeds,labels,xB,xF,beta) -> np.ndarray:
    # Perform segmentation on the subsampled data
    segmented_values = segment_image_3d(inputData, seeds, labels, xB, xF, beta)
    final_labels = apply_labels_3d(segmented_values, inputData, xB, xF)
    return final_labels

def calculate_weights_3d(image, beta=0.1):
    depth, height, width = image.shape
    num_voxels = depth * height * width
    indices = np.arange(num_voxels).reshape(depth, height, width)
    W = sp.dok_matrix((num_voxels, num_voxels))

    diffs = [
        np.abs(np.diff(image, axis=0)),
        np.abs(np.diff(image, axis=1)),
        np.abs(np.diff(image, axis=2))
    ]
    sigma = np.max([np.max(diff) for diff in diffs])
    if sigma == 0:
        sigma = 1
    beta_scaled = -beta / (2 * sigma**2)

    for k in range(depth):
        for i in range(height):
            for j in range(width):
                index = indices[k, i, j]
                neighbor_offsets = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]
                for dk, di, dj in neighbor_offsets:
                    nk, ni, nj = k + dk, i + di, j + dj
                    if 0 <= nk < depth and 0 <= ni < height and 0 <= nj < width:
                        neighbor_index = indices[nk, ni, nj]
                        weight = np.exp(beta_scaled * (image[k, i, j] - image[nk, ni, nj])**2)
                        W[index, neighbor_index] = weight

    return W.tocsr()

def segment_image_3d(image, seeds, labels, xB, xF, beta):
    depth, height, width = image.shape
    num_voxels = depth * height * width
    indices = np.arange(num_voxels).reshape(depth, height, width)

    W = calculate_weights_3d(image, beta)
    D = np.array(W.sum(axis=1)).flatten()
    L = sp.diags(D) - W
    L2 = L.dot(L)

    I_s = sp.lil_matrix((num_voxels, num_voxels))
    b = np.zeros(num_voxels)
    print("indices")
    print(indices.shape)
    print("seeds")
    print("---")
    #print(seeds)
    for (k, i, j), label in zip(seeds, labels):
        idx = indices[k, i, j]
        I_s[idx, idx] = 1
        b[idx] = xB if label == 'B' else xF

    A = I_s + L2
    print("Creacion del sistema")
    A = A.tocsc()  # Convert to CSC format for factorization
    print("Sistema convertido a csc")
    solve = factorized(A)
    print("Sistema factorizado")
    x = solve(b)
    print("Sistema resuelto")

    segmented_image = x.reshape((depth, height, width))
    return segmented_image

def apply_labels_3d(segmented_values, inputData, xB, xF):
    threshold = (xB + xF) / 2
    # Asignar etiquetas basado en el umbral
    labels = np.where(segmented_values >= threshold, xB, xF)
    return labels
