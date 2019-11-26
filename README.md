# image-segmentation-cluster

## Parallel Satellite Image Segmentation on Beowulf Cluster using MPI

Satellite Image processing is a very computationally intensive task. 

A [Beowulf Cluster](https://www-users.cs.york.ac.uk/~mjf/pi_cluster/src/Building_a_simple_Beowulf_cluster.html) is developed where there is one master node and one slave node. There is a shared file storage developed using Network File System (NFS) where the input satellite image is sent by client. 

Image segmentation is performed on this satellite image consisting of land area and crop area. The aim is to filter out the crop area which can be used for further data analytics.

This is a preview of the sample satellite image (inp.tif) of dimensions: 13244 x 14276 pixels. (size ≈ 700 MB) 

![Satellite Image](inp.PNG) 

This image is preprocessed by master node dividing it into many smaller chunks of images (224 x 224 pixels). For dividing the image into perfectly (224 x 224 pixel blocks), the satellite image is appended with pixels. The appends are made using pixels with value 255. Appropriate number of columns with pixel values of 255 are added to the right of the image and appropriate number of rows are added to the bottom of the image. The preprocessed images are stored in the [input_images](input_images) folder. 

![Chunk Image 1](input_images/1.png) ![Chunk Image 2](input_images/2.png) ![Chunk Image 3](input_images/3.png) 

Master and slave parallely perform image segmentation on all these smaller images and then the output images are clubbed back to form the full segmented image. These images serve as an input to image segmentation module. 

For image segmentation, a pretrained keras model [unet](https://github.com/zhixuhao/unet "Keras Model - unet") is used. This model takes input of 224x224 pixel images only, which is why preprocessing was required. Image segmentation is done on the Preprocessed images (here ≈ 3840 images), half of which are taken care by the Master and other half by the slave. Output images similar to these images are generated:

![Segmented Image 1](out_images/out1.png) ![Segmented Image 2](out_images/out2.png) ![Segmented Image 3](out_images/out3.png)
