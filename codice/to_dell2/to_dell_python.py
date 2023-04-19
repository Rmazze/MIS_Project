import serial

import time


ser = serial.Serial('COM4', 115200, timeout=1)
time.sleep(2) # wait for Arduino

i = 0

while (i < 10):
    # Serial write section
    ser.write(str("<V,a,t>").encode())
    time.sleep(1) # I shortened this to match the new value in your Arduino code

    # Serial read section
    msg = ser.read(ser.inWaiting()) # read all characters in buffer
    print("Message from arduino: ", msg.decode())
    i += 1