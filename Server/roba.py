import socket
import time

udpIP='127.0.0.1'
udpPort=5005
sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
pause=0.01
data=list(range(500,1500,10))
numIters=2
for i in range(0,numIters): # Loops numIters times
    for d in data: # For each element of data vector
        # d = struct.pack('!f',d)
        # sock.sendto(d, (udpIP, udpPort))
        sock.sendto(d.to_bytes(8, byteorder='big'), (udpIP, udpPort))
        print("sent: ", d)
        time.sleep(pause)