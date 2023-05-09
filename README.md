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
- If you are using this repo on a Pi4 remember to install pandas not through pip but through apt with <sudo apt-get install python-pandas>
- on the pi to run the redis server use <sudo systemctl enable /lib/systemd/system/redis-server.service>
- <python3 app.py --host=0.0.0.0> if it needs to be seen outside localhost
\\\
/etc/wpa_supplicant/wpa_supplicant.conf
/etc/dhcpcd.conf
\\\
use them to set up the network router there is a priority field use it to set up the order on which the Pi connects to the wifi

- sometimes the Pi doesnt recognize the behringer sound device at the start. Just detach and reattach the usb cable. This error is recognizable by a "*ALSA input error (snd_pcm_open): No such file or directory*" from pure data console


MIS@DISI

