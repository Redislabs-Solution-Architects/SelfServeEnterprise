from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from os import environ

import json

app = Flask(__name__)
bootstrap = Bootstrap()


nav = Nav()
topbar = Navbar('',
    View('Home', 'index'),
    View('Show', 'showdbs'),
    View('Create', 'createdb'),
    View('Delete', 'deletedb'),
)
nav.register_element('top', topbar)

redis_server = environ.get('REDIS_SERVER')
redis_server = environ.get('REDIS_USER')
redis_server = environ.get('REDIS_PASSWORD')

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/show')
def showdbs():
   return render_template('index.html')

@app.route('/create')
def createdb():
   return render_template('index.html')

@app.route('/delete')
def deletedb():
   return render_template('index.html')

if __name__ == '__main__':
   bootstrap.init_app(app)
   nav.init_app(app)
   app.run()
