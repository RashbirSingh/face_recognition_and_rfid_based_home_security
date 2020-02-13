#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 06:28:22 2020

@author: rashbir
"""
import pymysql
import re
import time
import serial
import os
from dotenv import load_dotenv

cwd = os.getcwd()
load_dotenv(cwd+"/.env")

class RFID():

    sql = 'CREATE DATABASE RFID'
    def __init__(self):
        self.RFID_dict = {}
        self.db = pymysql.connect(os.getenv("URL"),
                                  os.getenv("USER"),
                                  os.getenv("PASS"),
                                  os.getenv("DATABASE"))
        self.cursor = self.db.cursor()
        self.cwd = os.getcwd()

# =============================================================================
# 
# =============================================================================

    def executeSQL(self, sql):
        try:
            
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
    #        self.db.close()

# =============================================================================
# 
# =============================================================================

    def RFID_db(self,
                operation,
                name='NA',
                code='NA'):
        
        if operation == 'create':
            
            
            sql = """CREATE TABLE RFID (
            NAME  CHAR(20) NOT NULL,
            CODE INT(100) NOT NULL )"""
            print(sql)
            self.executeSQL(sql)
            
# =============================================================================
#             
# =============================================================================

        elif operation == 'insert':
            sql = """INSERT INTO RFID(NAME, CODE)
            VALUES ('"""+name+"""','"""+code+"""')"""
            print(sql)
            self.executeSQL(sql)
            
# =============================================================================
# 
# =============================================================================
            
        elif operation == 'match':
            ser = serial.Serial("/dev/ttyACM0",9600)
            ser.flushInput()
            sql = """SELECT * FROM RFID"""
            print(sql)
            self.executeSQL(sql)
            data = self.cursor.fetchall()
            for rows in data:
                self.RFID_dict[rows[0]] = rows[1]
                                                                                                                                                                                                                                                                                                                                                                                                                                                            
#            if name in self.RFID_dict.keys():
            for nameList in self.RFID_dict.keys():
                if re.match(name ,nameList, flags=re.I):
                    print('FOUND ',name)
                    ser.write(b"1")
                    return True
                else:
                    ser.write(b"2")
                    return False
#            return self.RFID_dict 

# =============================================================================
#           
# =============================================================================
      
    # def Create_RFID(self,
    #                 name,
    #                 RFID_code):
    #     self.RFID_dict[name] = RFID_code
    #     return self.RFID_dict
    
    # def match(self, name):
    #     if name in self.RFID_dict.keys() == True:
    #         print('open')
    
    