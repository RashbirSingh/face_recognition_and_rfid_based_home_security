#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 07:25:31 2020

@author: rashbir
"""

import os
from pythonFaceRecog import python_face_recognition
from RFID import RFID
import sys

rfid = RFID()

run = python_face_recognition()
if str(sys.argv[1]).lower() == 'encodecnn':
    run.encode( detection_method = 'cnn')
    
elif str(sys.argv[1]).lower() == 'encodehog':
    run.encode( detection_method = 'hog')

elif str(sys.argv[1]).lower() == 'recognise':
    run.recognise()
    
elif str(sys.argv[1]).lower() == 'card':
    action = input("Entre the action to perform: ")
    if action.lower() == 'insert':
        name = input("Entre user name: ")
        code = input("Entre user card code: ")
        print(rfid.RFID_db(action,
                           name,
                           code))
        
    if action.lower() == 'create':
        print(rfid.RFID_db(operation=action))
    
elif str(sys.argv[1]).lower() == 'data':
    cwd = os.getcwd()
    count = input("Entre the number of inputs: ")
    user = input("Entre the user name: ")
    os.mkdir(cwd + "/dataset/"+ user + "/"+ user.lower())
    for number in range(1, count+1):
        os.system("fswebcam --no-banner --no-timestamp -r 640x480" + cwd + \
                  "/dataset/"+ user.lower() + "/"+ user.lower()+str(number) +".jpg -S 30")

else:
    print('False Input')