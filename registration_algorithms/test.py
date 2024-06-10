import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import factorized
import nibabel as nib
import matplotlib.pyplot as plt

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
    for (k, i, j), label in zip(seeds, labels):
        idx = indices[k, i, j]
        I_s[idx, idx] = 1
        b[idx] = xB if label == 'B' else xF

    A = I_s + L2
    
    A = A.tocsc()  # Convert to CSC format for factorization
   
    solve = factorized(A)
    
    x = solve(b)

    segmented_image = x.reshape((depth, height, width))
    return segmented_image

def apply_labels_3d(segmented_values, xB, xF):
    threshold = (xB + xF) / 2
    labels = (segmented_values >= threshold).astype(int)
    labels = labels * xB + (1 - labels) * xF
    return labels

# Load and subsample the image data
img = nib.load('../file.nii')
full_data = img.get_fdata()

# Subsampling the data
factor = 5  # Subsampling factor, choose based on your data size and memory constraints
sampled_data = full_data[::factor, ::factor, ::factor]

# Parameters and seeds setup
seeds = [(0, 0, 0), (0, 0, 1), (9, 9, 9), (9, 9, 8)]
labels = ['B', 'B', 'F', 'F']
xB = 100
xF = 255
beta = 1.0

# Adjust seed positions according to the subsampling factor
adjusted_seeds = [(k//factor, i//factor, j//factor) for k, i, j in seeds]

# Perform segmentation on the subsampled data
segmented_values = segment_image_3d(sampled_data, adjusted_seeds, labels, xB, xF, beta)
final_labels = apply_labels_3d(segmented_values, xB, xF)

# Visualization
plt.imshow(final_labels[:, :, sampled_data.shape[2]//2], cmap='gray')  # Adjust the slice number as needed
plt.colorbar()
plt.show()