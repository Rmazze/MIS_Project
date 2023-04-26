import serial
import serial.tools.list_ports as ports
import time
from pythonosc import udp_client

teensyports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if "USB" in p.description
    ]
print(teensyports)
teensy_name = "USB"
#serialcom = serial.Serial('COM5',115200)
#serialcom.timeout = 1
#serialcom = serial.serial_for_url('rfc2217://localhost:4000',\

#f = float B = unsigned Char (uint8_t equivalent)

def disconnect(serialcom):
	serialcom.close()

def connect():
    print("mi sto connettendo")
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if teensy_name in p.description:
            teensy_port = p.device
            ser = serial.Serial(teensy_port, 115200)
    return ser

def pdSignal(serialcom):
    client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
    while True:
        msg = serialcom.read(serialcom.inWaiting()).decode('ascii')
        #if((len(msg) > 2) and not('AUD' in msg)):
        print(msg)
        if('AUDXX' in msg): 
            client.send_message("/x_state", 3)
            client.send_message("/x_state", 4)
            break
        if('AUDSX' in msg):
            client.send_message("/x_state", 3)
            break
        if('AUDDX' in msg):
            client.send_message("/x_state", 4)
            break

def connect():
    teensyports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if "USB" in p.description
    ]
    print(teensyports)
    serialcom = serial.Serial(teensyports[0],115200,timeout=5)
    return serialcom


def ResetMex():
    print("Gonna reset the system")
    serialcom.write(str('\"R\"').encode())

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

def test_vAt(serialcom):
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
    pdSignal(serialcom)


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


