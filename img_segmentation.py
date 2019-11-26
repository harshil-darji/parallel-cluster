from PIL import Image
import numpy as np
import keras
import os
import matplotlib.pyplot as plt
import cv2
from segmentation_models.metrics import iou_score
from segmentation_models.losses import bce_jaccard_loss
from mpi4py import MPI

# Master and slave start execution of same program together...
# To run this program you can use : mpiexec -hosts master,slave python3 /path/to/file/img_segmentation.py
# This will only run once Beowulf cluster is setup successfully.

comm = MPI.COMM_WORLD   # Defines the default communicator
num_procs = comm.Get_size()  # Stores the number of processes in size.
rank = comm.Get_rank()  # Stores the rank (pid) of the current process
stat = MPI.Status()

# Using keras model
model = keras.models.load_model('best_model.h5',custom_objects={'bce_jaccard_loss':bce_jaccard_loss, 'iou_score':iou_score})
print(model.summary())


if rank == 0:	# This will run only on Master node
	
	dir_path = 'input_images/'

	cnt = 1
	if cnt%2 == 0:
		for p in os.listdir(dir_path):
			imga = cv2.imread(dir_path + p)
			img = imga.reshape((1,224,224,3))
			out = model.predict(img)	# Model predicts crops here

			arr = np.where(out > 0.5, 255, 0).reshape(224,224)
			cv2.imwrite("out_images/out{}.png".format(str(cnt)),arr)	
			cnt += 1
			print("Running on Master")
			print(cnt)

else:			# This will run only on Slave node

	dir_path = 'input_images/'

	cnt = 1
	for p in os.listdir(dir_path):
		imga = cv2.imread(dir_path + p)
		img = imga.reshape((1,224,224,3))
		out = model.predict(img)		# Model predicts crops here

		arr = np.where(out > 0.5, 255, 0).reshape(224,224)
		cv2.imwrite("out_images/out{}.png".format(str(cnt)),arr)
		print("Running on Slave")
		cnt += 1
		print(cnt)