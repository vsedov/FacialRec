import os
import os.path  # new Stuff for of paths
import pathlib
import sys
import time  # Measure of time
from builtins import input

import cv2
from UnTrainedembeddings import embed

# embed = importlib.import_module('Facial Recognition/Main/Facial_Detection/main')

# module = importlib.import_module('.Facial_Detection.' + UnTrainedembeddings.py, package=__package__)
sys.path.insert(0, "/home/viv/GitHub/Facial Recognition/Main/Facial_Detection/")


def UpgradeFace(filename2, path, image):
    """UpgradeFace.

    Parameters
    ----------
    filename2 :
        filename2
    path :
        path
    image :
        image
    """
    # if  x0.jpg in file direcotry, meaning that the file exists
    if os.path.isfile(filename2):
        print("File exist")  # working
        counter = 1
        while True:
            counter += 1
            new_file_name = filename2.split(".jpg")[0] + str(counter) + ".jpg"
            if os.path.isfile(new_file_name):
                print("thiss is a new file", new_file_name)
                continue
                cv2.imwrite(os.path.join(path, filename2), image)
                break

            else:
                filename2 = new_file_name

                print("this is not a new file name" + filename2)

                cv2.imwrite(os.path.join(path, filename2), image)
                break

        # print(filename2)


def adding(dir, filename2, path, image):
    """adding.

    Parameters
    ----------
    dir :
        dir
    filename2 :
        filename2
    path :
    image :
        image
    """
    print("You have No Facial Data")
    filename2 = f"{n}.jpg"
    filename2 = os.path.join(path, filename2)

    path1 = "/home/viv/GitHub/Facial Recognition/Main/Images/"
    filename3 = f"{n}.jpg"

    print(filename2)  # need this to have a different file name
    cv2.imwrite(os.path.join(path, filename2), image)
    cv2.imwrite(os.path.join(path1, filename3), image)


def list_files(startpath):
    """list_files.

    Parameters
    ----------
    startpath :
        startpath
    """
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, "").count(os.sep)
        indent = " " * 4 * (level)
        print("{}{}/".format(indent, os.path.basename(root)))
        # subindent = ' ' * 4 * (level + 1)
        # for f in files:
        #   print('{}{}'.format(subindent, f))


def useroptionpath(path):
    """useroptionpath.

    Parameters
    ----------
    path :
        path
    """
    print("Liisting of path")
    print("Path to Direcotry", path)
    list_files(path)


def UPAD():
    video_capture = cv2.VideoCapture(0)

    imayes = str(
        input(
            "Do you want to add a face or upgrade facial data : Yes or No  ",
            "- This sytem will automaticly tell you if there is a user with your name\n",
        )
    )

    if (
        imayes.lower() == "yes"
    ):  # Accepts both types of input that has Upercase and lower case values

        # For functino useroption and listfile
        pathds = "/home/viv/GitHub/Facial Recognition/Main/Dataset/"

        usds = str(
            input(
                "do you want to have a listing of the path so you dont have any repeat of users\n"
            )
        )

        if usds.lower() == "yes":
            useroptionpath(pathds)

        elif usds.lower() == "No":
            var = str(
                input(
                    "are you use that you do not want the listing of the path  ?",
                    "  \n there is a chance of having the path repeated with new users",
                    "Each user is Case Sensitive \n",
                )
            )

            if var.lower() == "yes":
                return False
            elif var.lower() == "No":
                useroptionpath(pathds)

            else:
                print("no valid input has been made - program closing")
                exit()

        n = str(input("Enter your Name\nEnter"))

        t = time.time()
        print(
            "PLease Take as many PICTURES as you require - once done, please enter \n Q to exit \n Due to some hardware issues, Just spam q if single press does not work "
        )

        while True:

            return_value, image = video_capture.read()  # Creating a frame
            # detect faces in the grayscale frame

            # loop over the face detections and draw them on the frame

            cv2.imshow(
                "image", image
            )  # did not use gray for this as it is an overwrite and that the faces were not being Scanned
            if cv2.waitKey(25) & 0xFF == ord("s"):  # action taken

                # makes directory if user is not within it already
                pathlib.Path(
                    "/home/viv/GitHub/Facial Recognition/Main/Dataset/" + f"{n}"
                ).mkdir(parents=True, exist_ok=True)

                # Path to new direcotry taken.
                path = "/home/viv/GitHub/Facial Recognition/Main/Dataset/" + f"{n}/"

                # this just gets the list of directories that you have
                dir = os.listdir(path)
                filename2 = f"{n}.jpg"
                filename2 = os.path.join(path, filename2)
                # if this returns false, go to if statment
                UpgradeFace(filename2, path, image)

                if (
                    len(dir) == 0
                ):  # this would check if there is a face or not  -- WORKING
                    adding(dir, filename2, path, image)

            elif cv2.waitKey(50) & 0xFF == ord("q"):

                video_capture.release()
                cv2.destroyAllWindows()
                break

        video_capture.release()
        cv2.destroyAllWindows()
        print(time.time() - t)
        embed()  # time taken

    elif imayes.lower == "no":
        print("Thank you for your time, this program will now quit")
        exit()
    else:
        print("this input is not expecpted, please try again")


if "__main__" == __name__:
    UPAD()
