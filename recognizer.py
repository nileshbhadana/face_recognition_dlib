#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 05:07:25 2019

@author: nilesh
"""

#importing libraries
import cv2,pickle,face_recognition
font=cv2.FONT_HERSHEY_SIMPLEX

#laoding data files and storing in lists
with open("encodings.txt",'rb') as file_data:
    known_face_encodings=pickle.load(file_data)

with open("name.txt",'rb') as file_data:
    known_names=pickle.load(file_data)

cam=cv2.VideoCapture(0)
while cam.isOpened():
    frame=cam.read()[1]
    
    #converting BGR frame to RGB frame
    rgb_frame=frame[:,:,::-1]
    
    #gettting face locations
    face_locations=face_recognition.face_locations(rgb_frame)
    
    #getting face encodings
    current_face_encoding=face_recognition.face_encodings(rgb_frame,face_locations)
    
    for (top,right,bottom,left),face_encoding in zip(face_locations,current_face_encoding):
        
        #compariong face with known faces
        matches=face_recognition.compare_faces(known_face_encodings,face_encoding)
        name="unknown"
        
        if True in matches:
            #getting index for matched face
            match_index=matches.index(True)
            #getting name of the person
            name=known_names[match_index]
        
        cv2.rectangle(frame,(left,top),(right,bottom),(0,255,0),1)
        cv2.putText(frame, name, (left , top), font, 1.0, (255, 255, 255), 2)
        
    cv2.imshow("live",frame)
    
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
    
cam.release()
cv2.destroyAllWindows()