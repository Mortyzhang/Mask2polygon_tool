# Background

![image](https://user-images.githubusercontent.com/68632919/148710741-9ff1522c-cede-469e-8931-8751683b2506.png)

_A comparison of manually annotated datasets and automatically generated synthetic datasets. (The conventional method requires hand-made labeling of images to produce the training set, while our proposed system can automatically create synthetic data with instance annotations by using digital assets of CDT.)_

# How to use
**1. Converting the mask image into a COCO annotation for training the instance segmentation model.**<br />
This project is a tool to help transform the instance segmentation mask generated by unityperception into a polygon in coco format.

You can use unityperception to create synthetic masks of 3D models, instance segmentation or semantic segmentation. Currently unity does not release coco data format, this project is to facilitate users to convert the data format to coco format when training deep learning using synthetic data. If you like please give me stars, thanks.

**2. Dataset**<br />
Also, I wanna give an example for testing:

Here is the googledriver link that includes ground-turth and instance segmentation image, use the tool to transfer the mask into coco format for DCNNs training. https://drive.google.com/drive/folders/1nVt6AQDwCGoqNF7jf3ai2KSbLN2TC9xa?usp=sharing

# Some issues that may arise
Below are some problems you may meet.
There may be a problem when you use the datasets for training instance segmentation CNNs: You may get error in evaluation for instance segementation, like "File "pycocotools/_mask.pyx", in pycocotools._mask.frPyObjects cvat | Exception: input type is not supported.", 
because there are some seg [] in evaluation json file, please remove them, using replace [], .

If OSError: Could not find library geos_c or load any of its variants ['libgeos_c.so.1', 'libgeos_c.so'] Installed shapely using pip, and had the same problem. 
So I went ahead and installed it like so: sudo apt-get install libgeos-dev in Ubuntu os.

# Facade instance segmentation dataset
We present an instance segmentation dataset of building facade images collected in Tokyo and New York City, which includes 1271 images from street views that have been manually annotated.

**Download**<br />
Real-world dataset：
https://drive.google.com/drive/folders/1bJPfNTgNEU40lQHA5Rz0kQd18A_iOiPU?usp=sharing<br />
Synthetic dataset：
Please contact us
