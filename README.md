# image-segmentation-cluster

## Parallel Satellite Image Segmentation on Beowulf Cluster using MPI

Satellite Image processing is a very computationally intensive task. 

A [Beowulf Cluster](https://www-users.cs.york.ac.uk/~mjf/pi_cluster/src/Building_a_simple_Beowulf_cluster.html) is developed where there is one master node and one slave node. There is a shared file storage developed using Network File System (NFS) where the input satellite image is sent by client. 

Image segmentation is performed on this satellite image consisting of land area and crop area. The aim is to filter out the crop area which can be used for further data analytics.

First the satellite image is preprocessed by master node dividing it into many smaller chunks of images. Both nodes parallely perform image segmentation on all the smaller images and then the output images are clubbed back to form the full segmented image.

For image segmentation, a pretrained keras model [unet](https://github.com/zhixuhao/unet "Keras Model - unet") is used. This model takes input of 224x224 pixel images. Hence, the smaller images are resized to these dimensions and later fed to the keras model which detects the crop area.
