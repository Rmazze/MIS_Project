import serial
import serial.tools.list_ports as ports
import re

serialcom = serial.serial_for_url('rfc2217://localhost:4000', baudrate=115200)
#serialcom = serial.Serial('COM6',115200)
serialcom.write(b'<V,a,t>')

while True:
        ret = serialcom.readline()
        m = re.search('<(.+?)>', ret)
        print(m)
        if(ret == "a"):
             print("porcodio")
             break