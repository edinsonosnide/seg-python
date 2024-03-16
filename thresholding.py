'''
Thresholding Algorithm:
*data: the data after reading nii file. (I guess it works with other types of files if readed correctly)
*tau: int the number to make the thresholding of background and foreground
-> a matloblib image: <matplotlib.image.AxesImage at 0x785b9cc57160> for example
'''
import numpy as np


def algoThresholding(data: np.ndarray, tau: int ) -> None:
    img_th = data > tau
    print("tau choosen: ", tau)
    return img_th