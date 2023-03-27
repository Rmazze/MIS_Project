from flask import Flask, render_template, request
import pandas as pd
import csv

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('Main.html')

@app.route('/SignUp')
def signUp():
    return render_template('SignUp.html')


@app.route('/ErrorLogin')
def ErrorLogin():
    err_msg = "Invalid credentials"
    return render_template('ErrorLogin.html', err_msg = err_msg)

@app.route('/ErrorSignUp')
def ErrorSignUp():
    err_msg = "Username already in use"
    return render_template('ErrorSignUp.html', err_msg = err_msg)


# From login page go to start page or gives error
@app.route('/Start/', methods = ["POST", "GET"])
def startLogin():
    #controlla se c'è il nome, ritorna o una pagina o un'altra (errore)
    if request.method == 'GET':
        return f"The URL /Start is accessed directly. Try going to '/form' to submit form"
    
    if request.method == 'POST':
        # take form results
        form_data = request.form


        # check if form is empty
        if form_data["Username"]:
            if form_data["Password"]:
                
                # check if username exists
                with open('database/usr.csv', 'rt') as f:
                    reader = csv.reader(f, delimiter=';')
                    usr_exist = False
                    for row in reader:
                        if form_data["Username"] == row[0]:
                            usr_exist = True
                            # check if psw is correct
                            if form_data["Password"] == row[1]:
                                
                                # TODO capire cosa vogliamo fare e implementarlo
                                # apre il csv e per ora prende i risultati di marzo
                                with open('database/Prova.csv', 'rt') as f:
                                    reader_prova = csv.reader(f, delimiter=';')

                                    data = []
                                    data_bar = []
                                    labels = []
                                    chart_label = "March Trials: Reaction Time"
                                    for row in reader_prova:
                                        if row[6] == "03":
                                            data.append(row[1])
                                            data_bar.append(row[0])
                                            labels.append(row[5])
                                            

                                return render_template('Start.html', usr = form_data["Username"],  data = data, data_bar = data_bar, labels = labels, chart_label = chart_label)
                        
                            else:
                                msg = "Invalid password"
                                return render_template('ErrorLogin.html', msg = msg, msg_type = "error")
                            
                    # if no username is found, gives error       
                    if usr_exist is False:
                        msg = "Invalid credentials"
                        return render_template('ErrorLogin.html', msg = msg, msg_type = "error")

# From signup page create new credentials and go to login or gives error
@app.route('/Main/', methods = ["POST", "GET"])
def startSignUp():
    
    if request.method == 'POST':
        # take form results
        form_data = request.form

        # check if form is empty
        if form_data["Username"]:
            if form_data["Password"]:
                
                # check if username exists
                with open('database/usr.csv', 'rt') as f:
                    reader = csv.reader(f, delimiter=';')
                    usr_exist = False
                    for row in reader:
                        if form_data["Username"] == row[0]:
                            usr_exist = True
        
                    # if username exists, gives error       
                    if usr_exist:
                        err_msg = "Username already in use"
                        return render_template('ErrorSignUp.html', err_msg = err_msg)
                    
                    else:
                        # if username does not exist, add it to csv file
                        # transform dict to df to csv
                        df = pd.DataFrame.from_dict([form_data])
                        df.to_csv("database/usr.csv", sep=';', mode='a', index=False, header=False)

                        # go to login page
                        msg = "Account has been created"
                        return render_template('ErrorLogin.html', msg = msg, msg_type = "message")

@app.route('/Trial/', methods = ["POST", "GET"])
def startNewTrial():
    if request.method == 'POST':
        return render_template('Trial.html')


# Prova per capire come funziona il request.form non con il form ma con le opzioni
# Root endpoint
@app.route('/StartOr', methods = ["POST", "GET"])
def charts():
    if request.method == 'POST':
        print("OOOOOi")
        form_data = request.form.get('mycars')
        print(form_data)
        return render_template('Trial.html')


#TODO: fare funzione che scrive nel file csv i risultati delle prove con gli stimoli. Un file per utente



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')