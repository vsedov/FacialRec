import glob
import os
from builtins import input

import cv2
import face_recognition

video_capture = cv2.VideoCapture(0)

imayes = str(input("do you have an image ?\nPlease enter Yes || No || Exit "))


if imayes.lower() == "yes":

    print("Continue")

    known_face_encodings = []
    known_face_names = []

    pathds = glob.glob("/home/viv/GitHub/Facial Recognition/Main/Images/*.jpg")

    for path in pathds:
        image = face_recognition.load_image_file(path)
        known_face_encodings.append(face_recognition.face_encodings(image)[0])
        known_face_names.append(os.path.basename(path))

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        ret, frame = video_capture.read()

        small_frame = cv2.resize(
            frame, (0, 0), fx=0.25, fy=0.25
        )  # finding the face and the fram size

        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations
            )

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding
                )
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(
                frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED
            )
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(
                frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1
            )

        # Display the resulting image
        cv2.imshow("Video", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):  # press Q to exit
            break

    video_capture.release()
    cv2.destroyAllWindows()

else:
    print("Because you did not enter Yes or No the program will know quit ")
    quit()
