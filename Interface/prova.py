from flask import Flask, render_template, request
import pandas as pd
import csv

app = Flask(__name__)

# login page
@app.route('/')
def main():
    return render_template('Main.html')


# sign up page
@app.route('/SignUp')
def signUp():
    return render_template('SignUp.html')


# error login page
@app.route('/ErrorLogin')
def ErrorLogin():
    err_msg = "Invalid credentials"
    return render_template('ErrorLogin.html', err_msg = err_msg)


# error signup page
@app.route('/ErrorSignUp')
def ErrorSignUp():
    err_msg = "Username already in use"
    return render_template('ErrorSignUp.html', err_msg = err_msg)


# From login page go to trial page or to error page
@app.route('/Start/', methods = ["POST", "GET"])
def startLogin():
    
    # cannot be access directly
    if request.method == 'GET':
        return f"The URL /Start is accessed directly. Try going to '/form' to submit form"
    
    if request.method == 'POST':

        # take form results
        form_data = request.form

        # check if form is empty
        if form_data["Username"] and form_data["Password"]:
            
            # check if username exists
            with open('database/usr.csv', 'rt') as f:

                reader = csv.reader(f, delimiter=';')
                usr_exist = False

                for row in reader:
                    if form_data["Username"] == row[0]:
                    
                        usr_exist = True

                        # check psw: if right, go to trial page
                        if form_data["Password"] == row[1]:
                            return render_template('Start.html', usr = form_data["Username"])

                        # if psw is not right, go to error page
                        else:
                            msg = "Invalid password"
                            return render_template('ErrorLogin.html', msg = msg, msg_type = "error")
                        
                # if no corresponding usr is found, go to error page      
                if usr_exist is False:
                    msg = "Invalid credentials"
                    return render_template('ErrorLogin.html', msg = msg, msg_type = "error")

        # if user do not fill page, go to error page   
        else:           
            msg = "Please fill in the form"
            return render_template('ErrorLogin.html', msg = msg, msg_type = "error")

# From signup page create new credentials and go to login page or to error page
@app.route('/Main/', methods = ["POST", "GET"])
def startSignUp():
    
    if request.method == 'POST':

        # take form results
        form_data = request.form

        # check if form is empty
        if form_data["Username"] and form_data["Password"]:

            # check if username exists
            with open('database/usr.csv', 'rt') as f:

                reader = csv.reader(f, delimiter=';')
                usr_exist = False
                
                # check is usr is already in use
                # if so, go to erro page
                for row in reader:
                    if form_data["Username"] in row[0]:
                        usr_exist = True
                        err_msg = "Username already in use"
                        return render_template('ErrorSignUp.html', err_msg = err_msg)
    
                # if usr is not in use, create credentials
                if usr_exist is False:
   
                    # transform dict to df to csv
                    df = pd.DataFrame.from_dict([form_data])
                    df.to_csv("database/usr.csv", sep=';', mode='a', index=False, header=False)

                    # go to login page
                    msg = "Account has been created"
                    return render_template('ErrorLogin.html', msg = msg, msg_type = "message")

        else:           
            err_msg = "Please fill in the form"
            return render_template('ErrorSignUp.html', err_msg = err_msg)


@app.route('/Charts')
def charts():
    
    # take usr
    usr = request.args.get('usr', None)
    
    # open csv
    with open('database/results.csv', 'rt') as f:
        reader_prova = csv.reader(f, delimiter=';')

        allTime_c_data = []
        allTime_rt_data = []
        allTime_chart_label = []
        for row in reader_prova:
            # select only user results
            if row[6] == usr:
                allTime_c_data.append(row[0])
                allTime_rt_data.append(row[1])
                allTime_chart_label.append(row[5])

        # average of catch and reaction time
        allTime_c_data_int = [float(i) for i in allTime_c_data]
        allTime_rt_data_int = [float(i) for i in allTime_rt_data]
        c_avg = "{:.2f}".format(sum(allTime_c_data_int) / len(allTime_c_data_int)) + "%"
        rt_avg = "{:.2f}".format(sum(allTime_rt_data_int) / len(allTime_rt_data_int)) + " sec"

    # render Charts.html    
    return render_template('Charts.html', rt_avg = rt_avg, c_avg =c_avg, allTime_chart_label = allTime_chart_label, allTime_c_data = allTime_c_data, allTime_rt_data = allTime_rt_data)


#TODO: fare funzione che scrive nel file csv i risultati delle prove con gli stimoli. Un file per utente

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')