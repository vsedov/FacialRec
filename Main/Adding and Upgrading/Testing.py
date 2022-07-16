from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import pickle

from imutils.video import WebcamVideoStream
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import os

def main():
    # load our serialized face detector from disk
    print("[INFO] loading face detector...")
    protoPath = "/home/viv/GitHub/Facial Recognition/Main/Model/deploy.prototxt"
    modelPath = "/home/viv/GitHub/Facial Recognition/Main/Model/res10_300x300_ssd_iter_140000.caffemodel"

    detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)


    # load our serialized face embedding model from disk
    print("[INFO] loading face recognizer...")
    embedder = cv2.dnn.readNetFromTorch('/home/viv/GitHub/Facial Recognition/Main/Model/openface_nn4.small2.v1.t7')


    # load the actual face recognition model along with the label encoder
    recognizer = pickle.loads(open('/home/viv/GitHub/Facial Recognition/Main/output/recognizer.pickle', "rb").read())
    main = pickle.loads(open("/home/viv/GitHub/Facial Recognition/Main/output/main.pickle", "rb").read())

    # initialize the video stream, then allow the camera sensor to warm up
    print("starting video stream...")
    vs = WebcamVideoStream(src=0).start()
    time.sleep(2.0)

    # start the FPS throughput estimator
    fps = FPS().start()

    while True:
        frame = vs.read()

        frame = imutils.resize(frame, width=400)
        (h, w) = frame.shape[:2]

        # construct a blob from the image
        ib = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)), 1.0, (300, 300),
            (104.0, 177.0, 123.0), swapRB=False, crop=False)

        # apply OpenCV's deep learning-based face detector to localize
        # faces in the input image
        detector.setInput(ib)
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
                    (96, 96), (0,0, 0))
                embedder.setInput(faceBlob)
                vec = embedder.forward()




if __name__ == '__main__':
    main()