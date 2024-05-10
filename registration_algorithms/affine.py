from matplotlib import pyplot as plt
import SimpleITK as sitk
import numpy as np
def affine_registration_algo(data_fixed_path, data_rotated_path):
    # Cargar imágenes
    data_fixed = sitk.ReadImage(data_fixed_path, sitk.sitkFloat32)
    data_rotated = sitk.ReadImage(data_rotated_path, sitk.sitkFloat32)

    # Crear registro
    register = sitk.ImageRegistrationMethod()

    # Configurar transformación (afín)
    initial_transformation = sitk.CenteredTransformInitializer(data_fixed,
                                                              data_rotated,
                                                              sitk.AffineTransform(3),
                                                              sitk.CenteredTransformInitializerFilter.GEOMETRY)
    register.SetInitialTransform(initial_transformation)
    register.SetMetricFixedMask(data_fixed>0)

    # Configurar métrica de similitud
    register.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
    register.SetMetricSamplingStrategy(register.RANDOM)
    register.SetMetricSamplingPercentage(0.01)

    # Configurar optimizador
    register.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=100, convergenceMinimumValue=1e-6, convergenceWindowSize=10)
    register.SetOptimizerScalesFromIndexShift()

    # Realizar registro
    transformation = register.Execute(data_fixed, data_rotated)

    # Aplicar transformación a la imagen móvil
    data_rotated_registered = sitk.Resample(data_rotated, data_fixed, transformation, sitk.sitkLinear, 0.0, data_rotated.GetPixelID())

    # Muestrear la imagen móvil registrada en el espacio de la imagen móvil original
    data_rotated_registered_resample = sitk.Resample(data_rotated_registered, data_rotated)

    # Calcular la diferencia entre la imagen móvil original y la imagen móvil registrada muestreada
    difference = sitk.Abs(data_rotated_registered_resample - data_rotated)

    np_data_rotated_registered = sitk.GetArrayFromImage(data_rotated_registered)
    np_difference = sitk.GetArrayFromImage(difference)
    return np_data_rotated_registered, difference

# Ejemplo de uso
imagen_fija_path = './new_data.nii.gz'
imagen_movil_path = './new_data.nii.gz'
imagen_movil_registrada, diferencia = affine_registration_algo(imagen_fija_path, imagen_movil_path)
# Visualizar la diferencia entre la imagen móvil original y la imagen móvil registrada
plt.imshow(imagen_movil_registrada[:,90,:], cmap='gray')
plt.title('Imagen original')
plt.axis('off')
plt.show()