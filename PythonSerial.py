#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 02:40:04 2020

@author: rashbir
"""

import serial
ser = serial.Serial("/dev/ttyACM0",9600)
ser.flushInput()
ser.write(b"1")