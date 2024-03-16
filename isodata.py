'''
Isodata Algorithm:
*data: the data after reading nii file. (I guess it works with other types of files if readed correctly)
-> a matloblib image: <matplotlib.image.AxesImage at 0x785b9cc57160> for example
'''
import numpy as np
def isodataAlgo(data: np.ndarray) -> None:
    tau_init = 300
    t = 0
    tau_t = tau_init
    tolerancia = 0.001
    img_th = None
    while True:
        img_th = data > tau_t

        m_foreground = data[img_th == 1].mean()
        m_background = data[img_th == 0].mean()

        tau_new = 0.5 * (m_foreground + m_background)

        if abs(tau_new - tau_t) < tolerancia:
            break
        t = t + 1

        tau_t = tau_new

    return img_th