from PIL import Image
import numpy as np
import keras
import os
import matplotlib.pyplot as plt
import cv2

from segmentation_models.metrics import iou_score
from segmentation_models.losses import bce_jaccard_loss

# Remove limit on reading size of image
Image.MAX_IMAGE_PIXELS = None

# Read input Satellite image
im = Image.open('inp.tif')

imarray = np.array(im)

r,g,b = imarray[:,:,0], imarray[:,:,1],imarray[:,:,2]
gray= 0.2989*r + 0.5870*g + 0.114*b
shape = gray.shape

print(shape)

#60 196

# Image is 13244x14336 pixels. We need to divide this image into smaller blocks to send it to Master and Slave.
# The Keras model takes input of only 224x224 pixel images.
# So a padding of required number of pixels is done to successfuly divide the image into smaller chunks of 224x224 pixel blocks.

# Padding matrix for appending rows
app_r = np.zeros([1,13244])
app_r.fill(255)

for i in range(1,61):	#This range is set by dividing row pixels by 224 and adding one
    gray = np.vstack((gray,app_r)) #appending rows

print(gray.shape)

# Padding matrix for appending columns
app_c = np.zeros([14336,1])
app_c.fill(255)

for i in range(1,197):	#This range is set by dividing column pixels by 224 and adding one
    gray = np.column_stack((gray,app_c)) #appending columns

print(gray.shape)

#3840 images (64x60) are generated


imgwidth = gray.shape[1]
imgheight = gray.shape[0]

k=0

# Loop that generates 224x224 pixel sized images from input image
for i in range(0,imgheight,224):
    for j in range(0,imgwidth,224):
        path = 'input_images/'
        box = (j, i, j+224, i+224)
        a = im.crop(box)
        try:
            path = path+str(k+1)
            print(k)
            #o = a.crop(224*224)
            a.save(path,'png')
        except:
            pass
        k +=1

