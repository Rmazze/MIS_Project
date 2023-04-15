from flask import Flask, render_template, request
import pandas as pd
import csv
import random
import time

from pythonosc import udp_client

app = Flask(__name__)

@app.route('/index')
@app.route('/main')
@app.route('/')
def index():
    return render_template('Main.html')

@app.route('/signup')
def signup():
    return render_template('SignUp.html')

# From signup page, create new account or give errors
# TODO: sistemare
@app.route('/start', methods = ["POST","GET"])
def start():
    #controlla se c'è il nome, ritorna o una pagina o un'altra (errore)
    if request.method == 'GET':
        return f"The URL /Start is accessed directly. Try going to '/form' to submit form"
    
    if request.method == 'POST':
        # take form results
        form_data = request.form
        print("----------------------------------------------------")
        print(form_data)
        print("----------------------------------------------------")
        usr = form_data['username']
        print(usr)
        #psw = form_data['Password']

        # check if form is empty
        if form_data["username"]:
            if form_data["password"]:
                
                # TODO: check if username already exists, nel caso dire cambiare nome username o fare il login
                
                # vede se l'username è già stato usato o no
                # funziona ma forse si può usare direttamente panda diceva la chiara? ma non ho capito come
                with open('usr.csv', 'rt') as f:
                    reader = csv.reader(f, delimiter=';')
                    for row in reader:
                        if form_data["username"] == row[0]:
                            print(form_data["password"], "is in file")


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

def ClientPD():
  print('MyFlaskApp is starting up!')
  global client
  client = udp_client.SimpleUDPClient("127.0.0.1", 5005)


class PiApp(Flask):
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
            with self.app_context():
                ClientPD()
        super(PiApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)


app = PiApp(__name__)
app.run()