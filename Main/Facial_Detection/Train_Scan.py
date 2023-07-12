from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import pickle


from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import os
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import metrics


from imutils import paths


import logging
import matplotlib.pyplot as plt

from sklearn.model_selection import GridSearchCV
from sklearn.datasets import fetch_lfw_people
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import PCA

#STAGE 2 

def Scan():
# load the face embeddings
	print("loading face embeddings...")
	data = pickle.loads(open('/home/viv/GitHub/Facial Recognition/Main/output/embeddings.pickle', "rb").read())
	# encode the labels
	print("encoding labels...")
	main = LabelEncoder()
	labels = main.fit_transform(data["names"])



	print("training model...")



	recognizer = svm.SVC(C=77.00099999999999, break_ties=False, cache_size=200,
	class_weight='balanced', coef0=0.0001, decision_function_shape='ovr',
	degree=3, gamma='scale', kernel='sigmoid', max_iter=-1, probability=True,
	random_state=None, shrinking=True, verbose=False)


	recognizer.fit(data["embeddings"], labels)


	with open('/home/viv/GitHub/Facial Recognition/Main/output/recognizer.pickle', "wb") as f:
		f.write(pickle.dumps(recognizer))
	with open('/home/viv/GitHub/Facial Recognition/Main/output/main.pickle', "wb") as f:
		f.write(pickle.dumps(main))
	print("Loading Detector main - from path starting facial rec.")
	# load our serialized face detector from disk
	print("loading face detector...")
	protoPath = "/home/viv/GitHub/Facial Recognition/Main/Model/deploy.prototxt"
	modelPath = "/home/viv/GitHub/Facial Recognition/Main/Model/res10_300x300_ssd_iter_140000.caffemodel"

	detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)


	# load our serialized face embedding model from disk
	print("loading face recognizer...")
	embedder = cv2.dnn.readNetFromTorch('/home/viv/GitHub/Facial Recognition/Main/Model/openface_nn4.small2.v1.t7')


	# load the actual face recognition model along with the label encoder
	recognizer = pickle.loads(open('/home/viv/GitHub/Facial Recognition/Main/output/recognizer.pickle', "rb").read())
	le = pickle.loads(open("/home/viv/GitHub/Facial Recognition/Main/output/main.pickle", "rb").read())

	# initialize the video stream, then allow the camera sensor to warm up
	print("tarting video stream...")
	vs = VideoStream(src=0).start()
	time.sleep(2.0)

	# start the FPS throughput estimator
	fps = FPS().start()

	# loop over frames from the video file stream
	while True:
		# grab the frame from the threaded video stream
		frame = vs.read()

		# resize the frame to have a width of 600 pixels (while
		# maintaining the aspect ratio), and then grab the image
		# dimensions
		frame = imutils.resize(frame, width=600)
		(h, w) = frame.shape[:2]

		# construct a blob from the image
		imageBlob = cv2.dnn.blobFromImage(
			cv2.resize(frame, (300, 300)), 1.0, (300, 300),
			(104.0, 177.0, 123.0), swapRB=False, crop=False)

		# apply OpenCV's deep learning-based face detector to localize
		# faces in the input image
		detector.setInput(imageBlob)
		detections = detector.forward()

		# loop over the detections
		for i in range(0, detections.shape[2]):
			# extract the confidence (i.e., probability) associated with
			# the prediction
			confidence = detections[0, 0, i, 2]

			# filter out weak detections
			if confidence > 0.5:
				# compute the (x, y)-coordinates of the bounding box for
				# the face
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")

				# extract the face ROI
				face = frame[startY:endY, startX:endX]
				(fH, fW) = face.shape[:2]

				# ensure the face width and height are sufficiently large
				if fW < 20 or fH < 20:
					continue

				# construct a blob for the face ROI, then pass the blob
				# through our face embedding model to obtain the 128-d
				# quantification of the face
				faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
					(96, 96), (0, 0, 0), swapRB=True, crop=False)
				embedder.setInput(faceBlob)
				vec = embedder.forward()

				# perform classification to recognize the face
				preds = recognizer.predict_proba(vec)[0]
				j = np.argmax(preds)
				proba = preds[j]
				name = le.classes_[j]

				# draw the boun
				# ding box of the face along with the
				# associated probability
				text = "{}: {:.2f}%".format(name, proba * 100)
				y = startY - 10 if startY > 20 else startY + 10
				cv2.rectangle(frame, (startX, startY), (endX, endY),
					(0, 0, 255), 2)
				cv2.putText(frame, text, (startX, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)


		# update the FPS counter
		fps.update()

		# show the output frame
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

	# stop the timer and display FPS information
	fps.stop()
	print("elasped time: {:.2f}".format(fps.elapsed()))
	print(" approx. FPS: {:.2f}".format(fps.fps()))

	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()

if __name__ == '__main__':
	Scan()