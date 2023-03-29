from flask import Flask, render_template
from markupsafe import escape
#import RPi.GPIO as GPIO
app = Flask(__name__)
import argparse
import random
import time

from pythonosc import udp_client

#GPIO.setmode(GPIO.BCM)  # Sets up the RPi lib to use the Broadcom pin mappings
                        #  for the pin names. This corresponds to the pin names
                        #  given in most documentation of the Pi header

#GPIO.setwarnings(False) # Turn off warnings in the CLI

#GPIO.setup(2, GPIO.OUT) #GPIO2 ==> output

client = ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % escape(username)

@app.route('/user/<username>/round/<int:round_id>')
def show_post(username,post_id):
    # Check for user than begin relative numbered simulation //We count for each simulation in order to get the analytics
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

# Here is da sauce
# Per ogni richiest HTTP che arriva sotto forma di path <gpio/x/y> viene passata a pin=x con valore=y
# x/y possono essere qualsiasi valore. In caso di valore non convertibile da errore 404
@app.route('/gpio/<string:id>/<string:level>')
def setPinLevel(id, level):
    GPIO.output(int(id), int(level)) # messo int solo per giocare coi pin
    return "OK"

def ClientPD():
  print('MyFlaskApp is starting up!')
  client = udp_client.SimpleUDPClient("127.0.0.1", 5005)


class PiApp(Flask):
  def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
    if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
      with self.app_context():
        ClientPD()
    super(PiApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)


app = PiApp(__name__)
app.run()