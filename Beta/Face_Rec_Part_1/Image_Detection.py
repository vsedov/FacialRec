'''
Created on 14 Jun 2018

@author: vivsedov
'''


import face_recognition
from PIL import Image


image = face_recognition.load_image_file("260-83174-2016 - Multiple.jpg")
face_locations = face_recognition.face_locations(image)
print(f"I found {len(face_locations)} face(s) in this photograph.")


i = 0

for face_locations in face_locations:
    top, right, bottom, left = face_locations

    print(
        f" A face will be on the top{top} , Left{left} , Bottom{bottom}, Right {right}"
    )

    face_image = image[top:bottom, left:right]
    pil_image = Image.fromarray(face_image)
    pil_image.save(f"face-{i}.jpg")

    i = i +1


