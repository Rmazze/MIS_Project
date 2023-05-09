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

def pdSignal(serialcom, flag):
    client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
    while True:
        msg = serialcom.read(serialcom.inWaiting()).decode('ascii')
        #if((len(msg) > 2) and not('AUD' in msg)):
        if('AUDXX' in msg): 
            print(msg + " in pure data")
            if(flag):
                pdSignalFast()
            else:
                pdSignalSlow()
            client.send_message("/x_state", 3)# fast
            client.send_message("/x_state", 4)# slow
            break
        if('AUDSX' in msg):
            print(msg + " in pure data")
            client.send_message("/x_state", 3)
            break
        if('AUDDX' in msg):
            print(msg + " in pure data")
            client.send_message("/x_state", 4)
            break
        if('NOTAUD' in msg):
            print(msg + " in pure data")
            client.send_message("/x_state", 5)
            break
    #client.close()

def pdSignalHAP():
    client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
    client.send_message("/x_state", 2)

def pdSignalSAD():
    client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
    client.send_message("/x_state", 1)

def pdSignalFast():
    client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
    client.send_message("/x_state", 3)

def pdSignalSlow():
    client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
    client.send_message("/x_state", 4)
    #client.close()

def connect():
    while True:
        teensyports = [
            p.device
            for p in serial.tools.list_ports.comports()
            if "USB" in p.description
        ]
        print(teensyports)
        if(len(teensyports) > 0):
            serialcom = serial.Serial(teensyports[0],115200,timeout=5)
            break
        time.sleep(4)
    return serialcom


def ResetMex(serialcom):
    print("Gonna reset the system")
    recv = ""
    while True:
        serialcom.write(str('\"R\"').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting())
        recv = str(recv, 'ascii')
        print(recv)
        if("es" in recv):
            return True
        return False

def test_StimuliAudio():
    pdSignalFast()
    time.sleep(1)
    pdSignalSlow()

def test_StimuliVideo(serialcom):
    for x in range(3):
        serialcom.write(str('<P,V>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting())
        recv = str(recv, 'ascii')
        #if (not 'AUD' in recv):
        print(recv)
    #print("sono fuori")

def test_StimuliTactile(serialcom):
    recv = ""
    for x in range(3):
        serialcom.write(str('<P,T>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting())
        recv = str(recv, 'ascii')
        print(recv)
    #print("sono fuori")

def RecoverTime(serialcom):
    recv = ""
    while True:
        serialcom.write(str('<C>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting())
        recv = str(recv, 'ascii')
        print(recv)
        if('RES' in recv):
            break
    pdSignal(serialcom,True)
    return recv

def test_Vat(serialcom):
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
        if('2' in recv):
            break
        if('ate' in recv):
            break
    pdSignal(serialcom,True)

def test_vAtFast(serialcom):
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
        if('2' in recv):
            break
    pdSignal(serialcom,True)

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
        if('2' in recv):
            break
    pdSignal(serialcom, True)


def test_vaT(serialcom):
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
        if('2' in recv):
            break
    pdSignal(serialcom,True)

def test_VAt(serialcom):
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
        if('2' in recv):
            break
    pdSignal(serialcom, True)

def test_VaT(serialcom):
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
        if('2' in recv):
            break
    pdSignal(serialcom,True)


def test_vAT(serialcom):
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
        if('2' in recv):
            break
    pdSignal(serialcom, True)


def test_VAT(serialcom):
    recv = ""
    while True:
        serialcom.write(str('<V,A,T>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting())
        recv = str(recv, 'ascii')
        print(recv)
        if('0' in recv):
            break
        if('1' in recv):
            break
        if('2' in recv):
            break
    pdSignal(serialcom, True)

def test_vat(serialcom):
    recv = ""
    while True:
        serialcom.write(str('<v,a,t>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting())
        recv = str(recv, 'ascii')
        print(recv)
        if('0' in recv):
            break
        if('1' in recv):
            break
        if('2' in recv):
            break
    pdSignal(serialcom,True)

def test_video(serialcom):
    for x in range(6):
        serialcom.write(str('<P,V>').encode())
        time.sleep(1)