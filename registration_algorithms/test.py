import scipy.sparse as sp
from scipy.sparse.linalg import spsolve, factorized
import nibabel as nib
import numpy as np
img = nib.load('../file.nii')
data = img.get_fdata()
def calculate_weights_3d(image, beta=0.1):
    depth, height, width = image.shape
    num_voxels = depth * height * width
    indices = np.arange(num_voxels).reshape(depth, height, width)
    W = sp.lil_matrix((num_voxels, num_voxels))

    # Calculate maximum difference
    diffs = [
        np.abs(np.diff(image, axis=0)),
        np.abs(np.diff(image, axis=1)),
        np.abs(np.diff(image, axis=2))
    ]
    sigma = np.max([np.max(diff) for diff in diffs])

    if sigma == 0:
        sigma = 1

    for k in range(depth):
        for i in range(height):
            for j in range(width):
                index = indices[k, i, j]
                if k > 0:
                    W[index, indices[k - 1, i, j]] = np.exp(-beta * (image[k, i, j] - image[k - 1, i, j])**2 / sigma**2)
                if k < depth - 1:
                    W[index, indices[k + 1, i, j]] = np.exp(-beta * (image[k, i, j] - image[k + 1, i, j])**2 / sigma**2)
                if i > 0:
                    W[index, indices[k, i - 1, j]] = np.exp(-beta * (image[k, i, j] - image[k, i - 1, j])**2 / sigma**2)
                if i < height - 1:
                    W[index, indices[k, i + 1, j]] = np.exp(-beta * (image[k, i, j] - image[k, i + 1, j])**2 / sigma**2)
                if j > 0:
                    W[index, indices[k, i, j - 1]] = np.exp(-beta * (image[k, i, j] - image[k, i, j - 1])**2 / sigma**2)
                if j < width - 1:
                    W[index, indices[k, i, j + 1]] = np.exp(-beta * (image[k, i, j] - image[k, i, j + 1])**2 / sigma**2)

    return W
def segment_image_3d(image, seeds, labels, xB, xF, beta):
    depth, height, width = image.shape
    num_voxels = depth * height * width
    indices = np.arange(num_voxels).reshape(depth, height, width)

    W = calculate_weights_3d(image, beta)
    print("hola")
    D = np.array(W.sum(axis=1)).flatten()
    print("adios xd")
    L = sp.diags(D) - sp.csr_matrix(W)
    L2 = sp.csr_matrix(L.dot(L))

    I_s = sp.lil_matrix((num_voxels, num_voxels))
    b = np.zeros(num_voxels)
    for (k, i, j), label in zip(seeds, labels):
        idx = indices[k, i, j]
        I_s[idx, idx] = 1
        b[idx] = xB if label == 'B' else xF

    A = I_s + L2
    print("inicio factorized")
    A = sp.csr_matrix(A)
    print("A csr")
    solve = factorized(A.tocsc())
    print("fin factorized")
    x = solve(b)

    segmented_image = x.reshape((depth, height, width))
    return segmented_image

# Example seeds coordinates and labels for a 10x10x10 volume
seeds = [
    (0, 0, 0),  # Background seed
    (0, 0, 1),  # Background seed
    (9, 9, 9),  # Foreground seed
    (9, 9, 8)   # Foreground seed
]
labels = [
    'B',  # Background label
    'B',  # Background label
    'F',  # Foreground label
    'F'   # Foreground label
]

# Example parameters for labels
xB = 100  # Label value for background
xF = 255  # Label value for foreground
beta = 1.0  # Weight calculation parameter

def apply_labels_3d(segmented_values, xB, xF):
    # Calculate the threshold based on xB and xF
    threshold = (xB + xF) / 2

    # Assign labels based on the threshold
    labels = (segmented_values >= threshold).astype(int)
    labels = labels * xB + (1 - labels) * xF

    return labels

# Assume 'data' is a 3D numpy array of the medical image
segmented_values = segment_image_3d(data, seeds, labels, xB, xF, beta)
final_labels = apply_labels_3d(segmented_values, xB, xF)

# Visualizing a slice of the segmented image
import matplotlib.pyplot as plt
plt.imshow(final_labels[:, :, 5], cmap='gray')  # Visualize the 6th slice
plt.show()