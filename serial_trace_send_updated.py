#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 12:55:15 2023

@author: thilrasirfana
"""
#file for saving traces #be4 segment to 6 rounds of 20k
# file_locationT = "C:/Users/Work/Documents/Irfana/Python_Script/Traces"
# f=open(file_locationT, "w")  # create file
# f.close()

import binascii
from Crypto.Random import get_random_bytes
from typing import Any
import time
import serial
from numpy import ndarray

from osc_library import Lecroy
import numpy as np
from datetime import datetime
import h5py

# file_locationPT = "/Users/Work/Documents/Irfana/Python_Script/Texts/PT0.txt"
# file_locationCT = "/Users/Work/Documents/Irfana/Python_Script/Texts/CT0.txt"
# open(file_locationPT, "w") #clear file
# open(file_locationCT, "w")
# x=1

ser = serial.Serial('COM4',
                    baudrate=115200, parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS,
                    timeout=1)

OSC_IP_ADDRESS = '192.168.0.196'
CHANNEL = 'z1'

lecroy_if = Lecroy(ip_address=OSC_IP_ADDRESS)
lecroy_if.prepare_for_trace_capture()
lecroy_if.wait_lecroy()
file_locationPT = "/Users/Work/Documents/Irfana/Python_Script/Texts/PT.txt"
file_locationCT = "/Users/Work/Documents/Irfana/Python_Script/Texts/CT.txt"
open(file_locationPT, "w") #clear file
open(file_locationCT, "w")
##### End of the setup ####
#final_array = []
#tcounter = 0
#counter = 0
##sizecounter=0
##for i in range(1):
    #file_locationT = f"C:/Users/Work/Documents/Irfana/Python_Script/Traces{i}"
    #file_locationT = f"C:/Control Panel/Hardware and Sound/Devices and Printers/BUP Slim/Traces{i}"
    #file_locationT = f"E:/Traces/Traces{i}"
file_locationT = "C:/Users/Work/Documents/Irfana/Python_Script/Traces.h5"
    #f=open(file_locationT, "w")  # create file
final_array = []
tcounter = 0
counter = 0
    
def get_formatted_hex_string(value): #format string by 2 char = 1 byte
    formatted=''
    for i in range(0,32,2):
        formatted+= value[i]+value[i+1]+' '
    return formatted


c = 1000
NUMBER_OF_TRACES = c
while counter < c:
    plaintext=get_random_bytes(16)
    hexpt=binascii.hexlify(plaintext,' ')
    with open(file_locationPT, "ab") as file_PT : #append PT in file
                    file_PT.write(hexpt)
                    file_PT.write(b'\n')
    ser.write(plaintext)
    print('Start')
    endbyte = ser.read(16)  # Check for CT
    #time.sleep(1)
    #print(len(endbyte))
    if len(endbyte) == 16:
        print('Encryption has ended')
        hexct=binascii.hexlify(endbyte,' ')
        with open(file_locationCT, "ab") as file_CT :
                        file_CT.write(hexct)
                        file_CT.write(b'\n')
        counter += 1
        print(counter)
    else:
        print('No encryption')
        #counter = 200
    # sizecounter += 1
    # if sizecounter == 3000:
    #     file_locationPT = f"/Users/Work/Documents/Irfana/Python_Script/Texts/PT{x}.txt"
    #     file_locationCT = f"/Users/Work/Documents/Irfana/Python_Script/Texts/CT{x}.txt"
    #     open(file_locationPT, "w") #clear file
    #     open(file_locationCT, "w")
    #     x+= 1
    #     counter = 0

    ##### Collect 200 traces ####
    if tcounter == 0:
        ##### Collect one trace ####
        print('Before signal')
        _, interpreted_format = lecroy_if.get_native_signal_float(CHANNEL)
        print('After signal')
        # #be4append = datetime.now()
        # #print('be4 app=',be4append.strftime('%H:%M:%S'))
        # final_array.append(interpreted_format[:])
        # #x=f"final_array{i}"
        # #f"final_array{i}".append(interpreted_format[:])
        # aftappend = datetime.now()
        # print('aft app=',aftappend.strftime('%H:%M:%S'))
       # thisArray = np.asarray(interpreted_format[:]) #change trace to array format

        with h5py.File(file_locationT,'a') as hf: #open file for appending
            ar=np.asarray(interpreted_format[:]) #change trace to array format again #why?
            #hf.create_dataset("trace_data_set",(NUMBER_OF_TRACES,thisArray.shape[0])) #creates data set of given shape and dtype #dtype not specified here
            hf.create_dataset("trace_data_set", (NUMBER_OF_TRACES, ar.shape[0]))
            hf['trace_data_set'][tcounter]= ar #save trace
        tcounter += 1
    else:
        print('Before signal')
        _, interpreted_format = lecroy_if.get_native_signal_float(CHANNEL)
        print('After signal')

        # #final_array+f"{i}".append(interpreted_format[:])
        # final_array.append(interpreted_format[:])
        # #print('after append')
        # aftappend= datetime.now()
        # print('aft app=', aftappend.strftime('%H:%M:%S'))
        with h5py.File(file_locationT,'a') as hf:
            hf['trace_data_set'][tcounter]= numpy.asarray(interpreted_formt[:]) #save trace
        tcounter += 1
    # x=np.asarray(final_array, dtype=np.float16)
    # np.save(file_locationT,x)
    # print("saved")
    # print(x.shape)
    # del x

ser.close()

#np.save(file_locationT, np.asarray(final_array+f"{i}",dtype=np.float16))
#np.save(file_locationT, np.asarray(final_array,dtype=np.float16))
#x= np.load('traces.npy')
#print(x.shape)