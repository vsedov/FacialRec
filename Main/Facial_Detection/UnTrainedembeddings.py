from imutils import paths
import numpy as np
import imutils
import pickle
import cv2
import os
from cv2 import *

#STAGE1 


def embed():

	protoPath = "/home/viv/GitHub/Facial Recognition/Alpha/face_detection_model/deploy.prototxt"
	modelPath = "/home/viv/GitHub/Facial Recognition/Alpha/face_detection_model/res10_300x300_ssd_iter_140000.caffemodel"
	detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

	#  serialized face embedding model from disk
	print("loading face recognizer...") # GIVE A REASON FOR WHY YOU ARE NOT USING A HARS CASCADE AND WHY THIS IS AN ISSUE AND WHY IS THIS NOT AN ISSUE, WHAT ARE THE BENIFITS FOR THIS. 
	embedder = cv2.dnn.readNetFromTorch('/home/viv/GitHub/Facial Recognition/Alpha/openface_nn4.small2.v1.t7')

	print("quantifying faces...")
	path = list(paths.list_images('/home/viv/GitHub/Facial Recognition/Main/Dataset/'))
	print(path)

	knownEmbeddings = []
	knownNames = []

	max = 0
	for (i, path) in enumerate(path):

		name = path.split(os.path.sep)[-2]

		image = cv2.imread(path)
		image = imutils.resize(image, width=800)
		(h, w) = image.shape[:2]

		# construct a blob from the image
		ib = cv2.dnn.blobFromImage(  # ib =- image blob
			cv2.resize(image, (300, 300)), 1.0, (400, 400),
			(104.0, 177.0, 123.0), swapRB=False, crop=False)  # size of the image needed 

		# apply OpenCV's deep learning-based face detector to localize
		# faces in the input image
		detector.setInput(ib)
		detections = detector.forward()

		# ensure at least one face was found
		if len(detections) > 0:
			#  find the bounding box with the largest probability
			i = np.argmax(detections[0, 0, :, 2])
			confidence = detections[0, 0, i, 2]

			# weak detections - finding it 
			if confidence > 0.5 :


				# compute the (x, y)-coordinates of the bounding box for
				# the face


				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")

				# extract the face ROI and grab the ROI dimensions
				face = image[startY:endY, startX:endX]
				(fH, fW) = face.shape[:2]

				# ensure the face width and height are sufficiently large
				if fW < 20 or fH < 20:
					continue

				# construct a blob for the face ROI, then pass the blob
				# through our face embedding model to obtain the 128-d
				# quantification of the face
				fb = cv2.dnn.blobFromImage(face, 1.0 / 255,
					(96, 96), (0, 0, 0), swapRB=True, crop=False)
				embedder.setInput(fb)
				vec = embedder.forward()


				knownNames.append(name)
				knownEmbeddings.append(vec.flatten())
				max += 1

	# dump the facial embeddings + names to disk
	print(f" serializing {max} encodings...")
	data = {"embeddings": knownEmbeddings, "names": knownNames}
	with open('/home/viv/GitHub/Facial Recognition/Main/output/embeddings.pickle', "wb") as f:
		f.write(pickle.dumps(data))	

if __name__ == '__main__':
	embed()