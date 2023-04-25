import serial
import serial.tools.list_ports as ports
import time

teensyports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if "USB" in p.description
    ]
print(teensyports)
serialcom = serial.Serial(teensyports[0],115200,timeout=5)
#serialcom = serial.Serial('COM5',115200)
#serialcom.timeout = 1
#serialcom = serial.serial_for_url('rfc2217://localhost:4000',\

#f = float B = unsigned Char (uint8_t equivalent)

def hello():
    print("hello")

def ledOn():
    serialcom.write(str('on').encode())
    
def ledOff():
	serialcom.write(str('off').encode())

def disconnect():
	serialcom.close()

def connect():
    teensyports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if "USB" in p.description
    ]
    print(teensyports)
    serialcom = serial.Serial(teensyports[0],115200,timeout=5)
    return serialcom

def test_Vat():
    recv = ""
    while True:
        serialcom.write(str('<V,a,t>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting())
        recv = str(recv, 'ascii')
        print(recv)
        if('0' in recv):
            break
        if('1' in recv):
            break

def test_vAt():
    recv = ""
    while True:
        serialcom.write(str('<v,A,t>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting())
        recv = str(recv, 'ascii')
        print(recv)
        if('0' in recv):
            break
        if('1' in recv):
            break

def test_vaT():
    recv = ""
    while True:
        serialcom.write(str('<v,a,T>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting())
        recv = str(recv, 'ascii')
        print(recv)
        if('0' in recv):
            break
        if('1' in recv):
            break

def test_VAt():
    recv = ""
    while True:
        serialcom.write(str('<V,A,t>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting())
        recv = str(recv, 'ascii')
        print(recv)
        if('0' in recv):
            break
        if('1' in recv):
            break

def test_VaT():
    recv = ""
    while True:
        serialcom.write(str('<V,a,T>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting())
        recv = str(recv, 'ascii')
        print(recv)
        if('0' in recv):
            break
        if('1' in recv):
            break

def test_VAT():
    recv = ""
    while True:
        serialcom.write(str('<V,A;T>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting())
        recv = str(recv, 'ascii')
        print(recv)
        if('0' in recv):
            break
        if('1' in recv):
            break

def test_vAT():
    recv = ""
    while True:
        serialcom.write(str('<v,A,T>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting())
        recv = str(recv, 'ascii')
        print(recv)
        if('0' in recv):
            break
        if('1' in recv):
            break


