'''
Isodata Algorithm:
*data: the data after reading nii file. (I guess it works with other types of files if readed correctly)
-> a matloblib image: <matplotlib.image.AxesImage at 0x785b9cc57160> for example
'''
import numpy as np
def isodataAlgo(inputData: np.ndarray) -> np.ndarray:
    tau_init = 300
    t = 0
    tau_t = tau_init
    tolerancia = 0.001
    data = None
    while True:
        data = inputData > tau_t

        m_foreground = inputData[data == 1].mean()
        m_background = inputData[data == 0].mean()

        tau_new = 0.5 * (m_foreground + m_background)

        if abs(tau_new - tau_t) < tolerancia:
            break
        t = t + 1

        tau_t = tau_new

    return data