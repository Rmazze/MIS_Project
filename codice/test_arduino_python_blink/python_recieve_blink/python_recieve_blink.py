import serial
import time
import sys

ser = serial.Serial('COM3', 115200, timeout=1)
time.sleep(2)

try:
    while True:
        line = ser.readline()   # read a byte
        if line:
            string = line.decode()  # convert the byte string to a unicode string
            print(string)
            print("Current led state: ", string[11])
except KeyboardInterrupt:
    ser.close()
