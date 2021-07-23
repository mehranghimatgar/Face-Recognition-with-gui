from tkinter import *
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import face_recognition
import numpy as np
import os
import glob
def start () :
    global cap
    cap = cv2. VideoCapture ( 0 , cv2. CAP_DSHOW )
    display ()
def display () :
    global cap
    process_this_frame =0
    face_locations = []
    face_encodings = []
    face_names = []
    if cap is not None:
        ret, frame = cap. read ()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        if ret == True :
            if process_this_frame == 0:
                face_locations = face_recognition.face_locations( rgb_small_frame)
                face_encodings = face_recognition.face_encodings( rgb_small_frame, face_locations)
                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces (faces_encodings, face_encoding)
                    name = "Unknown"
                    face_distances = face_recognition.face_distance( faces_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = faces_names[best_match_index]
                    face_names.append(name)        
            process_this_frame = 1
            
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                frame = imutils. resize ( frame, width = 640 )
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                frame = imutils. resize ( frame, width = 640 )
                frame = cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                frame =cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                frame = cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            frame = imutils. resize ( frame, width = 640 )
            frame = cv2. cvtColor ( frame, cv2. COLOR_BGR2RGB )
            im = Image. fromarray ( frame )
            img = ImageTk. PhotoImage ( image = im )
            lblVideo. configure ( image = img )
            lblVideo. image = img
            lblVideo. after ( 10 , display )
        else :
            lblVideo. image = ""
            cap. release ()
            
def finish () :
    global cap
    cap. release () 
    
cap = None
faces_encodings = []
faces_names = []
cur_direc = os.getcwd()
path = os.path.join(cur_direc, 'data/')
List =glob.glob(path+'*.jpg')
number_files = len(List)
names = List.copy()
#==================train==========================
for i in range(number_files):
    globals()['image_{}'.format(i)] = face_recognition.load_image_file(List[i])
    globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]
    faces_encodings.append(globals()['image_encoding_{}'.format(i)])
    # Create array of known names
    names[i] = names[i].split(os.path.sep)[-1][:-4] 
    faces_names.append(names[i])


root = Tk ()
root.title("Face Recognition")
btnStart = Button ( root, text = "Start" , width = 45 , command = start )
btnStart. grid ( column = 0 , row = 0 , padx = 5 , pady = 5 )
btnFinalizar = Button ( root, text = "Finish" , width = 45 , command = finish )
btnFinalizar. grid ( column = 1 , row = 0 , padx = 5 , pady = 5 )
lblVideo = Label ( root )
lblVideo. grid ( column = 0 , row = 1 , columnspan = 2 )
root. mainloop ()    