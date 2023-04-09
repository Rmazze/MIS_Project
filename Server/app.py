from flask import Flask, render_template, request, session, url_for, send_from_directory
from flask_session import Session
import pandas as pd
import os
import csv
from celery import Celery, Task


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379"
#app.add_url_rule('/Favicon.ico', redirect_to=url_for('static', filename='Favicon.ico'))
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'Favicon.ico', mimetype='image/MIME')

celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)

@celery.task()
def add(x, y):
        return x + y

# admin page
@app.route('/Admin')
def admin():
    return render_template('Admin.html')

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


#TODO: fare funzione che scrive nel file csv i risultati delle prove con gli stimoli. Un file per utente

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')