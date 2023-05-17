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
    print("sto entrando nel wait della teensy")
    client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
    while True:
        try:
            msg = serialcom.read(serialcom.in_waiting).decode('ascii','ignore').strip()
            #if((len(msg) > 2) and not('AUD' in msg)):
            if('AUDSX' in msg):
                print(msg + " in pure data")
                if flag:
                    pdSignalFastSX()
                else:
                    pdSignalSlowSX()
                return "sx"
            elif('AUDDX' in msg):
                print(msg + " in pure data")
                if flag:
                    pdSignalFastDX()
                else:
                    pdSignalSlowDX()
                return "dx"
            elif('NOT' in msg): 
                print(msg + " in pure data")
                return "xx"
                print(msg + " in pure data")
                client.send_message("/x_state", 10)
                return "xx"
        except:
            return "Error with pure data"
    #client.close()

def pdSignalHAP():
    client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
    client.send_message("/x_state", 2)

def pdSignalSAD():
    client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
    client.send_message("/x_state", 1)

def pdSignalFastSX():
    client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
    client.send_message("/x_state", 3)

def pdSignalSlowSX():
    client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
    client.send_message("/x_state", 4)
    #client.close()

def pdSignalFastDX():
    client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
    client.send_message("/x_state", 5)

def pdSignalSlowDX():
    client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
    client.send_message("/x_state", 6)
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
        recv = serialcom.read(serialcom.inWaiting()).decode('ascii','ignore').strip()
        print(recv)
        if("es" in recv):
            return True
        return False

def test_StimuliAudio():
    pdSignalFastDX()
    time.sleep(1)
    pdSignalFastSX()
    time.sleep(1)
    pdSignalSlowDX()
    time.sleep(1)
    pdSignalSlowSX()

def test_StimuliVideo(serialcom):
    for x in range(3):
        serialcom.write(str('<P,V>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting()).decode('ascii','ignore').strip()
        #if (not 'AUD' in recv):
        print(recv)
    #print("sono fuori")

def test_StimuliTactile(serialcom):
    recv = ""
    for x in range(3):
        serialcom.write(str('<P,T>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting()).decode('ascii','ignore').strip()
        print(recv)
    #print("sono fuori")

def RecoverTime(serialcom):
    recv = ""
    for x in range (10):
        serialcom.write(str('<C>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting()).decode('ascii','ignore').strip()
        if('RES' in recv):
            break
    print(recv)
    return recv

def test_Vat(serialcom):
    recv = ""
    while True:
        serialcom.write(str('<V,a,t>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting()).decode('ascii','ignore').strip()
        #recv = str(recv, 'utf-8')
        st = recv
        print(st)
        print(recv)
        if('0' in recv):
            break
        if('1' in recv):
            break
        if('2' in recv):
            break
        if('ate' in recv):
            break
    return pdSignal(serialcom,True)

def test_vAtFast(serialcom):
    recv = ""
    while True:
        serialcom.write(str('<v,A,t>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting()).decode('ascii','ignore').strip()
        print(recv)
        if('0' in recv):
            break
        if('1' in recv):
            break
        if('2' in recv):
            break
    return pdSignal(serialcom,True)

def test_vAtSlow(serialcom):
    recv = ""
    while True:
        serialcom.write(str('<v,A,t>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting()).decode('ascii','ignore').strip()
        print(recv)
        if('0' in recv):
            break
        if('1' in recv):
            break
        if('2' in recv):
            break
    return pdSignal(serialcom,False)

def test_vAt(serialcom):
    recv = ""
    while True:
        serialcom.write(str('<v,A,t>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting()).decode('ascii','ignore').strip()
        print(recv)
        if('0' in recv):
            break
        if('1' in recv):
            break
        if('2' in recv):
            break
    return pdSignal(serialcom, True)


def test_vaT(serialcom):
    recv = ""
    while True:
        serialcom.write(str('<v,a,T>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting()).decode('ascii','ignore').strip()
        print(recv)
        if('0' in recv):
            break
        if('1' in recv):
            break
        if('2' in recv):
            break
    return pdSignal(serialcom,True)

def test_VAt(serialcom):
    recv = ""
    while True:
        serialcom.write(str('<V,A,t>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting()).decode('ascii','ignore').strip()
        print(recv)
        if('0' in recv):
            break
        if('1' in recv):
            break
        if('2' in recv):
            break
    return pdSignal(serialcom, True)

def test_VaT(serialcom):
    recv = ""
    while True:
        serialcom.write(str('<V,a,T>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting()).decode('ascii','ignore').strip()
        print(recv)
        if('0' in recv):
            break
        if('1' in recv):
            break
        if('2' in recv):
            break
    return pdSignal(serialcom,True)


def test_vAT(serialcom):
    recv = ""
    while True:
        serialcom.write(str('<v,A,T>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting()).decode('ascii','ignore').strip()
        print(recv)
        if('0' in recv):
            break
        if('1' in recv):
            break
        if('2' in recv):
            break
    return pdSignal(serialcom, True)


def test_VAT(serialcom):
    recv = ""
    while True:
        serialcom.write(str('<V,A,T>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting()).decode('ascii','ignore').strip()
        print(recv)
        if('0' in recv):
            break
        if('1' in recv):
            break
        if('2' in recv):
            break
    return pdSignal(serialcom, True)

def test_vat(serialcom):
    recv = ""
    while True:
        serialcom.write(str('<v,a,t>').encode())
        time.sleep(1)
        recv = serialcom.read(serialcom.inWaiting()).decode('ascii','ignore').strip()
        print(recv)
        if('0' in recv):
            break
        if('1' in recv):
            break
        if('2' in recv):
            break
    return pdSignal(serialcom,True)

def test_video(serialcom):
    for x in range(6):
        serialcom.write(str('<P,V>').encode())
        time.sleep(1)