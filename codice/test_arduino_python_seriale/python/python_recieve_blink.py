import serial
import time
import sys
import cv2

ser = serial.Serial('COM6', 115200, timeout=1)
#ser = serial.Serial('COM6', 115200)
time.sleep(2)

try:
    ser.write(str("<V,a,t>").encode())
    while True:
        line = ser.readline()   # read a byte
        if line:
            string = line.decode()  # convert the byte string to a unicode string
            print(string)
            #print("Current led state: ", string[11])
except KeyboardInterrupt:
    ser.close()
