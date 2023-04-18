from flask import Flask, render_template, request, session, url_for, send_from_directory
from flask_session import Session
from flask import jsonify
import serial
import serial.tools.list_ports as ports
from tasks import *
import random
import time
import threading
from pythonosc import udp_client
import pandas as pd
import os
import csv
from celery import Celery, Task

"""
Configuration
"""

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379"
#app.add_url_rule('/Favicon.ico', redirect_to=url_for('static', filename='Favicon.ico'))

celery = Celery(app.name,backend='redis://localhost:6379/0', broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)

#open only when using arduin0
ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)    
print("####")
#serialcom = serial.Serial('/dev/ttyACM0',9600)
#serialcom = serial.Serial('COM5',9600)
#serialcom.timeout = 1
serialcom = serial.serial_for_url('rfc2217://localhost:4000', baudrate=115200)


class NewThreadedTask(threading.Thread):
     def __init__(self):
         super(NewThreadedTask, self).__init__()
 
     def run(self):
         # run some code hereù
         readStream()
         print('Threaded task has been completed')



'''
General methods for building the business logic
'''
def ledOn():
    serialcom.write(str('on').encode())
    
def ledOff():
	serialcom.write(str('off').encode())

def disconnect():
	serialcom.close()

def dummyMex():
    print("sono dentro")
    serialcom.write(str('<V,a,t>').encode())
    serialcom.write(b'<V,a,t>')

def readStream():
    #print("ciao")
    ret = serialcom.readline()
    print(ret)
    if(ret == "b'N'"):
         print("boh")

#new_thread = NewThreadedTask()
#new_thread.start()

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
            #ledOff()

@celery.task()
def send_datum():
        client = udp_client.SimpleUDPClient("127.0.0.1", 5005)
        to_send = random.random()
        client.send_message("/filter", to_send)
        print("to_send: ", to_send)
        time.sleep(1)

@celery.task()
def add(x, y):
        return x + y

@celery.task(bind=True)
def longtest(self):
    """Background task that runs a long function with progress reports."""
    print("startmondo")
    dummyMex()
    readStream()
    print("hola")
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}


'''
Routing of the pages
'''

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'Favicon.ico', mimetype='image/MIME')

# admin page
@app.route('/Admin')
def admin():
    return render_template('Admin.html')

# login page
@app.route('/')
def main():
    return render_template('Test.html')

# sign up page
@app.route('/SignUp')
def signUp():
    return render_template('SignUp.html')


# error login page
@app.route('/ErrorLogin')
def errorLogin():
    err_msg = "Invalid credentials"
    return render_template('ErrorLogin.html', err_msg = err_msg)


# error signup page
@app.route('/ErrorSignUp')
def errorSignUp():
    err_msg = "Username already in use"
    return render_template('ErrorSignUp.html', err_msg = err_msg)

# sign up page
@app.route('/Questionnaire')
def questionnaire():
    return render_template('Questionnaire.html')


# From login page go to trial page or to error page
@app.route('/Trial/', methods = ["POST", "GET"])
def trialLogin():
    print(add(4,4))
    # cannot be access directly
    if request.method == 'GET':
        # take usr
        session["name"] = request.form.get("Username")
        return render_template('Trial.html')
    
    
    if request.method == 'POST':

        # take form results
        form_data = request.form
        session["name"] = request.form.get("Username")

        # check if form is empty
        if form_data["Username"] and form_data["Password"]:
            
            try:
                # read database
                df = pd.read_csv('database/usr.csv', sep = ";")

                # check if username exists
                if df[df["Username"] == form_data["Username"]].empty == False:

                    # check psw: if right, go to trial page
                    if df[(df["Username"] == form_data["Username"]) & (df["Password"] == form_data["Password"])].empty == False:
                        return render_template('Trial.html', usr = form_data["Username"])

                    # if psw is not right, go to error page
                    else:
                        msg = "Invalid password"
                        return render_template('ErrorLogin.html', msg = msg, msg_type = "error")
                            
                # if no corresponding usr is found, go to error page      
                else:
                    msg = "Invalid credentials"
                    return render_template('ErrorLogin.html', msg = msg, msg_type = "error")
                
            except:
                msg = "Invalid credentials"
                return render_template('ErrorLogin.html', msg = msg, msg_type = "error")

        # if user do not fill page, go to error page   
        else:           
            msg = "Please fill in the form"
            return render_template('ErrorLogin.html', msg = msg, msg_type = "error")

# From signup page create new credentials and go to login page or to error page
@app.route('/Login/', methods = ["POST", "GET"])
def trialSignUp():
    
    if request.method == 'POST':

        # take form results
        form_data = request.form

        # check if form is empty
        if form_data["Username"] and form_data["Password"]:

            try: 
                # read database
                df = pd.read_csv('database/usr.csv', sep = ";")

                # check is usr is already in use
                # if so, go to erro page
                if df[df["Username"] == form_data["Username"]].empty == False:
                    err_msg = "Username already in use"
                    return render_template('ErrorSignUp.html', err_msg = err_msg)
        
                # if usr is not in use, create credentials
                else:
                    # transform dict to df to csv
                    new_user = pd.DataFrame.from_dict([form_data])
                    new_user.to_csv("database/usr.csv", sep = ';', mode = 'a', index = False, header = ["Username", "Password"])

                    # go to login page  
                    msg = "Account has been created"
                    return render_template('ErrorLogin.html', msg = msg, msg_type = "message")
            
            except:
                # transform dict to df to csv
                new_user = pd.DataFrame.from_dict([form_data])
                new_user.to_csv("database/usr.csv", sep = ';', mode = 'a', index = False, header = ["Username", "Password"])

                # go to login page
                msg = "Account has been created"
                return render_template('ErrorLogin.html', msg = msg, msg_type = "message")

        else:           
            err_msg = "Please fill in the form"
            return render_template('ErrorSignUp.html', err_msg = err_msg)


# charts
@app.route('/Charts')
def charts():
    
    # take usr
    usr = session["name"]

    try:
        # read database
        df = pd.read_csv('database/results.csv', sep = ";")

        # check is usr has already done trials
        #if df[df["Username"] == usr].empty == False:
        allTime_c_data =  df[df["Username"] == usr]["Catch"].values.tolist() # list that contains wheter the user has catch the ball or not
        allTime_rt_data = df[df["Username"] == usr]["ReactionTime"].values.tolist() # list that contains the reaction time of the user
        allTime_chart_label = df[df["Username"] == usr]["Date"].values.tolist() # list that contains the date of the trials

        # average of catch and reaction time
        allTime_c_data_int = [float(i) for i in allTime_c_data]
        allTime_rt_data_int = [float(i) for i in allTime_rt_data]
        c_avg = "{:.2f}".format(sum(allTime_c_data_int) / len(allTime_c_data_int)) + "%"
        rt_avg = "{:.2f}".format(sum(allTime_rt_data_int) / len(allTime_rt_data_int)) + " sec"
    
    except:
        allTime_chart_label = []
        allTime_c_data = []
        allTime_rt_data = []
        c_avg = "0%"
        rt_avg = "0 sec"
        

    # render Charts.html    
    return render_template('Charts.html', usr = usr, rt_avg = rt_avg, c_avg =c_avg, allTime_chart_label = allTime_chart_label, allTime_c_data = allTime_c_data, allTime_rt_data = allTime_rt_data)


@app.route("/test", methods=["POST"])
def run_task():
    task = longtest.apply_async()
    if task.result == 42:
         print()
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}

#Introduced for debugging purposes
@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = longtest.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'SUCCESS':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)

#TODO: fare funzione che scrive nel file csv i risultati delle prove con gli stimoli. Un file per utente

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')