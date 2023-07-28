from flask import Flask, render_template, request
import serial
import serial.tools.list_ports as ports
import pandas as pd
import csv
import random
import time

from pythonosc import udp_client
from celery import Celery, Task

app = Flask(__name__)
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379"

celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)

ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)    
print("####")
#serialcom = serial.Serial('/dev/ttyACM0',9600)
serialcom = serial.Serial('COM5',9600)
serialcom.timeout = 1

'''
General methods for building the business logic
'''
def ledOn():
    serialcom.write(str('on').encode())
    
def ledOff():
	serialcom.write(str('off').encode())

def disconnect():
	serialcom.close()


'''
Celery part
All the methods inside here are related to the asynchronous part.
Possibly all channels and serials need to be invoked here in order to interfere
with the overall process

NOTE: seems like serial does not interfere with the overall process
'''

@celery.task()
def add(x, y):
        return x + y

@celery.task()
def send_data():
        client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
        for x in range(10):
            to_send = random.random()
            client.send_message("/filter", to_send)
            print("to_send: ", to_send)
            ledOn()
            time.sleep(1)
            ledOff()

@celery.task()
def send_datum():
        client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
        to_send = random.random()
        client.send_message("/filter", to_send)
        print("to_send: ", to_send)
        time.sleep(1)

'''
Routing of the pages
'''

@app.route('/hello')
def add_task():
    send_data()
    return "Hello World! I'm using Flask."

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'on' in request.form.to_dict():
            ledOn()
            send_datum()
        if 'off' in request.form.to_dict():
            ledOff()
        if 'dis' in request.form.to_dict():
            disconnect()

    #if request.form['off']:
    #	print('asdfdsafsdfasf')
    return render_template('index.html')


def ClientPD():
    print('MyFlaskApp is starting up!')

if __name__ == "__main__":
    #ClientPD()
    app.run()

@app.route("/lollobrigifa")
def home():
    return "Hello World! I'm using Flask."
    """
    for x in range(10):
        to_send = random.random()
        client.send_message("/filter", to_send)
        print("to_send: ", to_send)
        time.sleep(1)
    """
    return "Hello World! I'm using Flask."
