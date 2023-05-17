# MIS_Project

AA 2022/2023

## Members

Roberto Mazzaro
Laura Corso
Noemi Canovi
Mattia Carolo

## Topic

Analyze reflex phenomena through multisensory interactive sustems

### Development tips

- Always specigy the backend lib on the configuration
- Since we are working async the celery call will be celery -A app.celery worker --loglevel=info --pool threads
- If you are using this repo on a Pi4 remember to install pandas not through pip but through apt with 'sudo apt-get install python-pandas'
- on the pi to run the redis server use <sudo systemctl enable /lib/systemd/system/redis-server.service>
- <python3 app.py --host=0.0.0.0> if it needs to be seen outside localhost
\\\
/etc/wpa_supplicant/wpa_supplicant.conf
/etc/dhcpcd.conf
\\\
use them to set up the network router there is a priority field use it to set up the order on which the Pi connects to the wifi

If on celery terminal you see 'First char' in loop detach the teensyboard since we are on a loop bug

MIS@DISI

### Can You run it

In order 

### How To Start

>> Windows

1) access through terminal to the PI (it should be connected to the local network) with SSH
2) Once inside launch the server with the command 'vncserver'. It should build the address at the same IP with the port 1
3) Access through 'vnc viewer' to the PI

> PI Launch

- go to path $:> MIS_project>Server
- launch python3 app.py --host=0.0.0.0
- launch celery -A app.celery worker --loglevel=info --pool threads
- launch pd (not with &)
- check audio in test audio e media
- launch Main_osc
