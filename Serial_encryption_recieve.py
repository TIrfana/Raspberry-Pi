import serial
import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import RPi.GPIO as GPIO


ser=serial.Serial ('/dev/serial0',115200,
bytesize=serial.EIGHTBITS,
parity=serial.PARITY_NONE, 
stopbits=serial.STOPBITS_ONE, 
timeout=1) 


file_locationPT = "/home/pi/Documents/PT.txt" 
file_locationCT = "/home/pi/Documents/CT.txt"
open(file_locationPT, "w") #clear file
open(file_locationCT, "w")


while 1:
    time.sleep(0.05)
    x=ser.read()
    print(x)
    if x == b's' :
        #run encryption
        key = b'1234567891234567' #generate key

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(18,GPIO.OUT)

        def get_formatted_hex_string(value): #format string by 2 char = 1 byte
            formatted=''
            for i in range(0,32,2):
                formatted+= value[i]+value[i+1]+' '
            return formatted

        x=0 
        while x<1:
            time.sleep(1)
              
            plaintext=get_random_bytes(16) 
            #print(plaintext)
            
            cipher = AES.new(key, AES.MODE_ECB) #Set up AES
            GPIO.output(18,GPIO.LOW)
            
            cipertext= cipher.encrypt(plaintext)
            GPIO.output(18,GPIO.HIGH)
              
            hexpt=get_formatted_hex_string(plaintext.hex())
            hexct=get_formatted_hex_string(cipertext.hex())
            #print(hexpt)
            #print(hexct)
            
            with open(file_locationPT, "a") as file_PT : #append PT in file
                            file_PT.write(hexpt+'\n')
            with open(file_locationCT, "a") as file_CT :
                            file_CT.write(hexct+'\n')
           
            print('The ciphertext is',cipertext)
            x+=1
                    
            GPIO.cleanup() #set pin back to default   
            file_PT.close()
            file_CT.close()
    ser.write(b'e')


