import argparse
import logging
# from sklearn.svm import train_auto
import multiprocessing
import os
import pickle
import time

import cv2
import imutils
import matplotlib.pyplot as plt
import numpy as np
from imutils.video import FPS, VideoStream
from sklearn import metrics, preprocessing, svm
from sklearn.datasets import fetch_lfw_people
from sklearn.decomposition import PCA
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

# STAGE 2

# load the face embeddings


def main():

    print("[INFO] loading face embeddings...")
    data = pickle.loads(
        open(
            "/home/viv/GitHub/Facial Recognition/Main/output/embeddings.pickle", "rb"
        ).read()
    )
    # encode the labels
    print("[INFO] encoding labels...")
    main = LabelEncoder()
    labels = main.fit_transform(data["names"])

    # train the model used to accept the 128-d embeddings of the face and
    # then produce the actual face recognition
    print("[INFO] training model...")

    # there is an improvment  from 1 - 2.22
    # recognizer = svm.SVC(C = 50,kernel="linear", probability=True ,class_weight='balanced')

    # AFTER YOU MAKE FACIAL REC ON PROJECT
    # recognizer = svm.SVC(C = 10,kernel="rbf", probability=True ,class_weight='balanced')

    # recognizer = svm.SVC(C=100, break_ties=False, cache_size=200, class_weight='balanced', coef0=0.0,
    # decision_function_shape='ovr', degree=3, gamma='scale', kernel='rbf',
    # max_iter=-1, probability=False, random_state=None, shrinking=True,
    # tol=0.001, verbose=False)

    # setting algorithm parameters

    # param =  dict(kernel="rbf",svm_type=cv2.SVM_C_SVC,c=1)

    # recognizer = cv2.SVM.train_auto((data["embeddings"], labels, params = params)

    # recognizer = cv2.SVM.train_auto()

    # recognizer = svm.SVC(C = 10, kernel="sigmoid",probability=True ,class_weight='balanced',coef0 =0.459912)  # optiised function/.

    # cv2.SVM.predict(data["embeddings"],[labels])

    """
    recognizer = svm.SVC(C=17.000999999999998, break_ties=False, cache_size=200,
    class_weight='balanced', coef0=0.0, decision_function_shape='ovr', degree=3,
    gamma='scale', kernel='rbf', max_iter=-1, probability=True,
    random_state=None, shrinking=True, tol=0.001, verbose=False)
    """
    # param_grid = {'C': [0.01, 0.1, 1, 10, 100], 'kernel': ['rbf']}

    """
        a = np.arange(0.001,100)
        b = np.arange(0.001,100)#

        print(a,b)

        #print(a)


        param_grid = {'C': a,'coef0':b,'kernel': ['sigmoid']}

        recognizer = GridSearchCV(SVC(class_weight='balanced',probability=True), param_grid,n_jobs=12)
        recognizer.fit(data["embeddings"], labels)
        #print(classification_report(data["embeddings"], labels))
        print(recognizer.best_estimator_)
    """

    recognizer = svm.SVC(
        C=77.00099999999999,
        break_ties=False,
        cache_size=200,
        class_weight="balanced",
        coef0=0.0001,
        decision_function_shape="ovr",
        degree=3,
        gamma="scale",
        kernel="sigmoid",
        max_iter=-1,
        probability=True,
        random_state=None,
        shrinking=True,
        verbose=False,
    )

    recognizer.fit(data["embeddings"], labels)

    with open("/home/viv/GitHub/Facial Recognition/Main/output/recognizer.pickle", "wb") as f:
        f.write(pickle.dumps(recognizer))
    with open("/home/viv/GitHub/Facial Recognition/Main/output/main.pickle", "wb") as f:
        f.write(pickle.dumps(main))


if __name__ == "__main__":
    main()
