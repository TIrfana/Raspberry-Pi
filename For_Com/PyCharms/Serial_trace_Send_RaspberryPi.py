#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 12:55:15 2023

@author: thilrasirfana
"""

from typing import Any
import time
import serial
from osc_library import Lecroy
import numpy as np
from datetime import datetime
import h5py


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

file_locationT = "C:/Users/Work/Documents/Irfana/Python_Script/Traces.h5"
   
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
    ser.write(b's')
    print('Start')
    endbyte = ser.read()

    if endbyte== b'e':
        print('Encryption has ended')
        counter += 1
        print(counter)
    else:
        print('No encryption')


    ##### Collect traces ####
    if tcounter == 0:
        ##### Collect one trace ####
        print('Before signal')
        _, interpreted_format = lecroy_if.get_native_signal_float(CHANNEL)
        print('After signal')

        with h5py.File(file_locationT,'a') as hf: #open file for appending
            ar=np.asarray(interpreted_format[:]) #change trace to array format again #why?
            hf.create_dataset("trace_data_set", (NUMBER_OF_TRACES, ar.shape[0]))
            hf['trace_data_set'][tcounter]= ar #save trace
        tcounter += 1
    else:
        print('Before signal')
        _, interpreted_format = lecroy_if.get_native_signal_float(CHANNEL)
        print('After signal')

        with h5py.File(file_locationT,'a') as hf:
            hf['trace_data_set'][tcounter]= np.asarray(interpreted_formt[:]) #save trace
        tcounter += 1


ser.close()

