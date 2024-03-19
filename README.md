# Medical Images (NIFTI) analizer
I have created a program in python that can be used to process and segmentate 
mediacal images in the NIFTI format.
## Instalation
1. Make sure you have python > 3 installed
2. Clone my repository: https://github.com/EdinsonUwU/seg-python
3. Enter to the folder seg-python-main
```bash
cd seg-python-main
```
2. Create a virtual environment for the project's dependencies
```bash
virtualenv venv
```
3. Activate the just created virtual environment
```bash
source venv/bin/activate
```
4. Install all the dependencies in the environment running:
```bash
pip install -r requirements.txt
```
## Run
To run the program use something like vs code or pycharm (recomended).
If you are in the console run:
```bash
python3 main.py
```
## You can do
* Upload a nifti file
* Draw annotations on a view mode and slice that you can define
* Clear annotations
* Go forth and backwards on all the segmentations you have done
* Change slice
* Change mode (Coronal, Sagital, Axial)
* Look up the state of the segmentation: processing, and finished.
* Run segmentation algorithms: Thresholding, isodata, region growing, k-means
## Screenshots
First image after running the program
![First window](screenshots/first_image.png)
Uploading a Medical Image (nifti file)
![First window](screenshots/upload_nifti_button.png)
File successfully uploaded
![First window](screenshots/uploaded_nifti.png)
Change between sagital, coronal, axial view, and change the slice
![First window](screenshots/view_mode_and_slices.png)
Change color and annotate
![First window](screenshots/color.png)
Clear all annotations
![First window](screenshots/clear_annotations.png)
Run thresholding (you have to choose a value to do it)
![First window](screenshots/thresholding.png)
![First window](screenshots/thresholding_result.png)
Go back to the prior fdata
![First window](screenshots/go_back.png)
Run isodata (Global thresholding)
![First window](screenshots/isodata.png)

