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

# From signup page, create new account or give errors
# TODO: sistemare
@app.route('/Start/', methods = ["POST", "GET"])
def startOrError():
    #controlla se c'è il nome, ritorna o una pagina o un'altra (errore)
    if request.method == 'GET':
        return f"The URL /Start is accessed directly. Try going to '/form' to submit form"
    
    if request.method == 'POST':
        # take form results
        form_data = request.form

        #usr = form_data['Username']
        #psw = form_data['Password']

        # check if form is empty
        if form_data["Username"]:
            if form_data["Password"]:
                
                # TODO: check if username already exists, nel caso dire cambiare nome username o fare il login
                
                # vede se l'username è già stato usato o no
                # funziona ma forse si può usare direttamente panda diceva la chiara? ma non ho capito come
                with open('usr.csv', 'rt') as f:
                    reader = csv.reader(f, delimiter=';')
                    for row in reader:
                        if form_data["Username"] == row[0]:
                            print(form_data["Username"], "is in file")


                # if username is not already used, add it to csv file
                # transform dict to df to csv
                df = pd.DataFrame.from_dict([form_data])
                print ("Input DataFrame is:", df)
                df.to_csv("usr.csv", sep=';', mode='a', index=False, header=False)

                # enter start.html
                return render_template('Start.html', form_data = form_data)
            
        else:
            #TODO add msg "complete form to continue" e sistemare
            return render_template('ErrorUsr.html', form_data = form_data)

#TODO From Login page, check if username and psw are correct and go to start trials or gives error
#@app.route('/mettinomecheserve/', methods = ["POST", "GET"])
#def mettinomecheservecoerente()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')