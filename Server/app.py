from flask import Flask, render_template, request, session, url_for, send_from_directory
from flask_session import Session
from flask import jsonify
import serial
import serial.tools.list_ports as ports
from tasks import *
import random
import time
import datetime
import threading
from pythonosc import udp_client
import pandas as pd
import os
import csv
import re
from celery import Celery, Task, states
from celery.exceptions import Ignore
from teensy import *

"""
Configuration
"""

Ntest = 0

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#Session(app)
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379"
#app.add_url_rule('/Favicon.ico', redirect_to=url_for('static', filename='Favicon.ico'))
Session(app)
celery = Celery(app.name,backend='redis://localhost:6379', broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)

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

@celery.task(bind=True)
def command_task(self,command,user):
    serialcom = connect()
    side = ""
    print("la stringa arrivata e " + command)
    if('<V,A,T>' in command):
        print("Starting all test")
        side = test_VAT(serialcom)
    elif('<v,A,t,1>' in command):
        print("Starting all test")
        side =test_vAtSlow(serialcom)
    elif('<v,A,t,2>' in command):
        print("Starting all test")
        side =test_vAtFast(serialcom)
    elif('<V,a,t>' in command):
        print("Starting Visual test")
        side =test_Vat(serialcom)
    elif('<v,A,t' in command):
        print("Starting audio test")
        side =test_vAt(serialcom)
    elif('<v,a,T>' in command):
        print("Starting tactile test")
        side =test_vaT(serialcom)
    elif('<V,A,t>' in command):
        print("Starting Visual/audio test")
        side =test_VAt(serialcom)
    elif('<V,a,T>' in command):
        print("Starting Visual/tactile test")
        side =test_VaT(serialcom)
    elif('<v,A,T>' in command):
        print("Starting all test")
        side =test_vAT(serialcom)
        
    print(side)
    eject_flag = False
    data = {}

    start_time = time.time()

    while True:
        ret = serialcom.readline(serialcom.in_waiting).decode('ascii','ignore').strip()
        #st = str(ret, 'ascii')
        st = ret
        if(not 'AUD' in st):
            print(st)
        if("eta" in st):
            print("palla staccara")
            eject_flag = True
            self.update_state(state='EJECTED',
                          meta={'current': Ntest, 'total': 8,
                                'status': "test numero: " + str(Ntest)})
        if(("SAD" in st) or ("efa" in st) or ("irs" in st)):
            self.update_state(
                state = states.FAILURE,
                meta={'current': 1, 'total': 8,
                                'status': "FAIL"}
            )
            disconnect(serialcom)
            pdSignalSAD()
            time.sleep(1)
            data = {'catch': [0], 'reactionTime': [0]}
            if(list(command)[1] == 'V'):
                data['Visual'] = [1]
            else:
                data['Visual'] = [0]
            if(list(command)[3] == 'A'):
                if('<v,A,t,1>' in command):
                    data['Audio'] = [2]
                else:
                    data['Audio'] = [1]
            else:
                data['Audio'] = [0]
            if(list(command)[5] == 'T'):
                data['Tactile'] = [1]
            else:
                data['Tactile'] = [0]
            data['Date'] = [str(datetime.date.today())]
            data['us'] = [user]
            resultsFillFailure(data)
            raise Ignore()
        if("es" in st):
            self.update_state(
                state = states.FAILURE,
                meta={'current': 1, 'total': 8,
                                'status': "FAIL"}
            )
            disconnect(serialcom)
            pdSignalSAD()
            time.sleep(1)
            raise Ignore()
        if("HAP" in st):
            print(st)
            disconnect(serialcom)
            numbers = re.findall(r'\d+',st)
            print(numbers)
            num1 = '{:,.3f}'.format(float(numbers[0])).rstrip('0').rstrip('.')
            num1 = num1.replace(',', '.') 
            if float(num1) > 40:
                num1 = '0,' + str(num1)
                num1 = num1.replace(',', '.') 
                num1 = float(num1)
            num2 = '{:,.3f}'.format(float(numbers[1])).rstrip('0').rstrip('.')
            num2 = num2.replace(',', '.') 
            if float(num2) > 40:
                num2 = '0,' + str(num2)
                num2 = num2.replace(',', '.') 
                num2 = float(num2)
            pdSignalHAP()
            if(float(num1) > float(num2)):
                data['catch'] = [1]
                data['reactionTime'] = [float(num1)]
            else:
                data = {'catch': [1], 'reactionTime': [float(num2)]}
            if(list(command)[1] == 'V'):
                data['Visual'] = [1]
            else:
                data['Visual'] = [0]
            if(list(command)[3] == 'A'):
                if('<v,A,t,1>' in command):
                    data['Audio'] = [2]
                else:
                    data['Audio'] = [1]
            else:
                data['Audio'] = [0]
            if(list(command)[5] == 'T'):
                data['Tactile'] = [1]
            else:
                data['Tactile'] = [0]
            data['Date'] = [str(datetime.date.today())]
            data['us'] = [user]
            resultsFillSuccess(data)
            return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'timer1': num1, 'timer2': num2}
        

        if time.time() > start_time + 3:
            recv = RecoverTime(serialcom)
            sx = 0
            dx = 0
            if 'RES' in recv:
                pattern = r"RES sx:(\d+)\|dx:(\d+)"
                match = re.search(pattern, recv)
                if match:
                    sx = float(match.group(1))
                    dx = float(match.group(2))
                num1 = sx / 1000
                num2 = dx / 1000
                if(num1 == 0 and num2 == 0):
                    self.update_state(
                    state = states.FAILURE,
                    meta={'current': 1, 'total': 8,
                                    'status': "FAIL"}
                    )
                    disconnect(serialcom)
                    pdSignalSAD()
                    time.sleep(1)
                    data = {'catch': [0], 'reactionTime': [0]}
                    if(list(command)[1] == 'V'):
                        data['Visual'] = [1]
                    else:
                        data['Visual'] = [0]
                    if(list(command)[3] == 'A'):
                        if('<v,A,t,1>' in command):
                            data['Audio'] = [2]
                        else:
                            data['Audio'] = [1]
                    else:
                        data['Audio'] = [0]
                    if(list(command)[5] == 'T'):
                        data['Tactile'] = [1]
                    else:
                        data['Tactile'] = [0]
                    data['Date'] = [str(datetime.date.today())]
                    data['us'] = [user]
                    resultsFillFailure(data)
                    raise Ignore()
                print(recv)
                pdSignalHAP()
                if(float(num1) > float(num2)):
                    data['catch'] = [1]
                    data['reactionTime'] = [float(num1)]
                else:
                    data = {'catch': [1], 'reactionTime': [float(num2)]}
                if(list(command)[1] == 'V'):
                    data['Visual'] = [1]
                else:
                    data['Visual'] = [0]
                if(list(command)[3] == 'A'):
                    if('<v,A,t,1>' in command):
                        data['Audio'] = [2]
                    else:
                        data['Audio'] = [1]
                else:
                    data['Audio'] = [0]
                if(list(command)[5] == 'T'):
                    data['Tactile'] = [1]
                else:
                    data['Tactile'] = [0]
                data['Date'] = [str(datetime.date.today())]
                data['us'] = [user]
                resultsFillSuccess(data)
                return {'current': 100, 'total': 100, 'status': 'Task completed!',
                'timer1': num1, 'timer2': num2}
            else:
                self.update_state(
                state = states.FAILURE,
                meta={'current': 1, 'total': 8,
                                'status': "FAIL"}
                )
                disconnect(serialcom)
                pdSignalSAD()
                time.sleep(1)
                data = {'catch': [0], 'reactionTime': [0]}
                if(list(command)[1] == 'V'):
                    data['Visual'] = [1]
                else:
                    data['Visual'] = [0]
                if(list(command)[3] == 'A'):
                    if('<v,A,t,1>' in command):
                        data['Audio'] = [2]
                    else:
                        data['Audio'] = [1]
                else:
                    data['Audio'] = [0]
                if(list(command)[5] == 'T'):
                    data['Tactile'] = [1]
                else:
                    data['Tactile'] = [0]
                data['Date'] = [str(datetime.date.today())]
                data['us'] = [user]
                resultsFillFailure(data)
                raise Ignore()

        #send_datum()
        self.update_state(state='PROGRESS',
                            meta={'current': 1, 'total': 8,
                                    'status': "test numero: " + str(Ntest)})

@celery.task()
def reset():
    print("reset")
    serialcom = connect()
    ResetMex(serialcom)
    return {'reset': True}

@celery.task()
def audiocue():
    print("Test audio stimuli")
    test_StimuliAudio()
    return {'reset': True}

@celery.task()
def videocue():
    print("Testing video stimuli")
    serialcom = connect()
    test_StimuliVideo(serialcom)
    return {'reset': True}

@celery.task()
def hapticcue():
    print("Testing haptic stimuli")
    serialcom = connect()
    test_StimuliTactile(serialcom)
    return {'reset': True}

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

"""
# cues page
@app.route('/Cues')
def cues():
    return render_template('Cues.html')
"""

# trial page
@app.route('/Trial')
def trial():
    return render_template('Trial.html')

# test page
@app.route('/Test')
def test():
    return render_template('Test.html')

# login page
@app.route('/')
def main():
    return render_template('Login.html')

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


# From login page go to cues page or to error page
@app.route('/Cues', methods = ["POST", "GET"])
def cuesLogin():
    # cannot be access directly
    if request.method == 'GET':
        # take usr
        session["name"] = request.form.get("Username")
        return render_template('Cues.html')
    
    
    if request.method == 'POST':

        # take form results
        form_data = request.form
        session["name"] = request.form.get("Username")
        print(session["name"])

        # check if form is empty
        if form_data["Username"] and form_data["Password"]:
            
            try:
                # read database
                df = pd.read_csv('database/usr.csv', sep = ";")

                # check if username exists
                if df[df["Username"] == form_data["Username"]].empty == False:

                    # check psw: if right, go to cues page
                    if df[(df["Username"] == form_data["Username"]) & (df["Password"] == form_data["Password"])].empty == False:
                        session['name'] = form_data["Username"]
                        return render_template('Cues.html', usr = form_data["Username"])

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
@app.route('/Login', methods = ["POST", "GET"])
def loginSignUp():
    
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
                    new_user.to_csv("database/usr.csv", sep = ';', mode = 'a', index = False, header = False)

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
    print(usr)

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


@app.route("/trial", methods=["POST"])
def command_test():
    data = request.get_json() # retrieve the data sent from JavaScript
    print(data)
    # process the data using Python code
    result = data['value']
    print(result)
    usr = session["name"]
    print(usr)
    task = command_task.delay(result,usr)    
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}

@app.route("/audio", methods=["POST"])
def audiocue_test():
    # process the data using Python code
    task = audiocue.apply_async()    
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}

@app.route("/video", methods=["POST"])
def videocue_test():
    # process the data using Python code
    task = videocue.apply_async()    
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}

@app.route("/haptic", methods=["POST"])
def hapticcue_test():
    # process the data using Python code
    task = hapticcue.apply_async()    
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}

@app.route("/reset", methods=["POST"])
def reset_task():
    task = reset.apply_async()
    print("reset")
    #time.sleep(1000)
    return jsonify({}), 202, {'Location': 0}


#Introduced for debugging purposes
@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = command_task.AsyncResult(task_id)
    if task.state == 'SUCCESS':
        print(task.info)
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'timer1' in task.info:
            print("ciao")
            response['timer1'] = task.info['timer1']
        if 'timer2' in task.info:
            print("2ciao")
            response['timer2'] = task.info['timer2']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 0,
            'total': 0,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)

#TODO: fare funzione che scrive nel file csv i risultati delle prove con gli stimoli. Un file per utente

def resultsFillSuccess(data):
    if 'results.csv' in os.listdir('database'):
        # create a dictionary with the informations
        #new_data = {'catch': 1, 'reactionTime': [form_data["rt"]], 'Visual': [form_data["visual"]], 'Audio': [form_data["aptic"]], 'Tactile': [form_data["tactile"]], 'Date': [str(datetime.date.today())], 'us': [session['name']]}

        # convert the dictionary to dataframe
        print(data)
        #myFile = open('database/results.csv', 'r+')
        #writer = csv.writer(myFile)
        new_data = pd.DataFrame.from_dict(data)
        #writer.writerow(data.values())
        #myFile.close()

        # save in csv
        new_data.to_csv('database/results.csv', sep = ';', mode = 'a', index = False, header = False)
    
    else:
        # create a dictionary with the informations
        #new_data = {'catch': [form_data["catch"]], 'reactionTime': [form_data["rt"]], 'Visual': [form_data["visual"]], 'Audio': [form_data["aptic"]], 'Tactile': [form_data["tactile"]], 'Date': [str(datetime.date.today())], 'us': [session['name']]}

        # convert the dictionary to dataframe
        new_data = pd.DataFrame.from_dict(data)

        # save in csv
        new_data.to_csv('database/results.csv', sep = ';', mode = 'a', index = False, header = ["Catch", "ReactionTime", "C_Visual", "C_Auditory", "C_Tactile", "Date", "Username"])

def resultsFillFailure(data):
    if 'results.csv' in os.listdir('database'):
        # create a dictionary with the informations
        #new_data = {'catch': [form_data["catch"]], 'reactionTime': [form_data["rt"]], 'Visual': [form_data["visual"]], 'Audio': [form_data["aptic"]], 'Tactile': [form_data["tactile"]], 'Date': [str(datetime.date.today())], 'us': [session['name']]}
        # convert the dictionary to dataframe
        new_data = pd.DataFrame.from_dict(data)

        # save in csv
        new_data.to_csv('database/results.csv', sep = ';', mode = 'a', index = False, header = False)
    
    else:
        # create a dictionary with the informations
        #new_data = {'catch': [form_data["catch"]], 'reactionTime': [form_data["rt"]], 'Visual': [form_data["visual"]], 'Audio': [form_data["aptic"]], 'Tactile': [form_data["tactile"]], 'Date': [str(datetime.date.today())], 'us': [session['name']]}
        # convert the dictionary to dataframe
        new_data = pd.DataFrame.from_dict(data)

        # save in csv
        new_data.to_csv('database/results.csv', sep = ';', mode = 'a', index = False, header = ["Catch", "ReactionTime", "C_Visual", "C_Auditory", "C_Tactile", "Date", "Username"])



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')