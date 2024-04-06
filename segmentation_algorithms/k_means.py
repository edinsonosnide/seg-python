import numpy as np
import math

def algoKMeans(data: np.ndarray,k: int) -> np.ndarray:

    #Get the one-dimensional array of all intensities.
    oneDimensionArray = data.flatten()

    #Delete all duplicates
    oneDimensionSet = set(oneDimensionArray)

    #Convert to array again
    oneDimensionArray = list(oneDimensionSet)

    # Use np.random.choice to select k unique integer centroids from the data
    centroids = np.random.choice(oneDimensionArray, k, replace=False)

    #Here will be store all the centroids with the closest items to them
    clusterStorage = dict()

    #maximum algo iterations
    maxIterations = 3

    for _ in range(maxIterations):

        clusterStorage.clear() # all the items putted in relation to the previuos centroids are worhtless

        #initialize the clusterStorage keys, there will be k keys
        for i in centroids:
            clusterStorage[i] = []

        #fill the items to the keys: it will put each item of data to its centroid
        for i in oneDimensionArray:
            min_difference = math.inf
            closest_centroid = None
            for j in centroids:
                if min_difference > abs(j-i):
                    min_difference = abs(j-i)
                    closest_centroid = j
            clusterStorage[closest_centroid] = clusterStorage[closest_centroid] + [i]

        #clear the array with the current centroids
        centroids = []

        #set the new centroids
        for i in clusterStorage.keys():
            try:
              centroids.append(int(np.mean(clusterStorage[i])))
            except:
              print("error- cluster empty")

    #having the final centroids edit the data of the nifti file accordignly
    for i in range(data.shape[0]):
      for j in range(data.shape[1]):
        for k in range(data.shape[2]):
          min_difference = math.inf
          closest_centroid = None
          for c in centroids:
              if min_difference > abs(c-data[i][j][k]):
                  min_difference = abs(c-data[i][j][k])
                  closest_centroid = c
          data[i][j][k] = closest_centroid

    return data