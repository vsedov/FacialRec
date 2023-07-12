import cv2
import glob
import os
from cv2.cv2 import CamShift
import face_recognition
from builtins import input
import numpy as np 


#new Stuff for import of paths  
import os.path
from os import path
import pathlib
import time # Measure of time 
from os.path import isfile

video_capture = cv2.VideoCapture(0) 


imayes =str(input("Do you want to add a face or upgrade facial data : Yes or No  - This sytem will automaticly tell you if there is a user with your name\n"))



if imayes.lower() == "yes": #Accepts both types of input that has Upercase and lower case values 

    pathds = '/home/viv/GitHub/Facial Recognition/Main/Dataset/' # For functino useroption and listfile

    n = str(input("Enter your Name\nEnter"))

    t = time.time()
    print("PLease Take as many PICTURES as you require - once done, please enter \n Q to exit \n Due to some hardware issues, Just spam q if single press does not work ")


    while True:

    #Most worked path 

        return_value,image = video_capture.read() #Creating a frame 
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        cv2.imshow('image',gray)
        if cv2.waitKey(25)& 0xFF == ord('s'): #action taken 


            pathlib.Path(
                f"/home/viv/GitHub/Facial Recognition/Main/Dataset/{n}"
            ).mkdir(parents=True, exist_ok=True)

            path = f"/home/viv/GitHub/Facial Recognition/Main/Dataset/{n}/"

            dir = os.listdir(path) # this just gets the list of directories that you have
            filename2 = f"{n}.jpg"
            filename2= os.path.join(path , filename2)
            if os.path.isfile(filename2): #if  x0.jpg in file direcotry, meaning that the file exists
                print ("File exist") # working
                counter  = 1
                while True:
                    counter  += 1
                    new_file_name = filename2.split(".jpg")[0] + str(counter ) + ".jpg" # 
                    if os.path.isfile(new_file_name):
                        print("thiss is a new file",new_file_name)
                        continue
                    else:
                        filename2 = new_file_name

                        print(f"this is not a new file name{filename2}")

                        cv2.imwrite(os.path.join(path , filename2),image)
                        break

            if len(dir) == 0: # this would check if there is a face or not  -- WORKING 
                print("You have No Facial Data")      
                filename2 = f"{n}.jpg"
                filename2= os.path.join(path , filename2)

                print(filename2) # need this to have a different file name
                cv2.imwrite(os.path.join(path , filename2),image)



        elif cv2.waitKey(50)  & 0xFF == ord('q'):

            video_capture.release()
            cv2.destroyAllWindows()
            break

    video_capture.release()
    cv2.destroyAllWindows()
    print (time.time()-t) # time taken

elif imayes.lower =="no":
    print("Thank you for your time, this program will now quit")
    exit()
else:
    print("this input is not expecpted, please try again")

