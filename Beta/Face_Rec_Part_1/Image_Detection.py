'''
Created on 14 Jun 2018

@author: vivsedov
'''

import face_recognition
from PIL import Image


image = face_recognition.load_image_file("260-83174-2016 - Multiple.jpg")
face_locations = face_recognition.face_locations(image)
print("I found {} face(s) in this photograph.".format(len(face_locations)))


i = 0

for face_locations in face_locations:
    top, right, bottom, left = face_locations

    print(" A face will be on the top{} , Left{} , Bottom{}, Right {}".format(top,left,bottom,right))

    face_image = image[top:bottom, left:right]
    pil_image = Image.fromarray(face_image)
    pil_image.save("face-{}.jpg".format(i))

    i = i +1


