from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from os import environ

import json
import requests

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
redis_user = environ.get('REDIS_USER')
redis_password = environ.get('REDIS_PASSWORD')

def delete_database(server, user, password, id):
   headers = { 'Content-Type' : 'application/json'}
   u = 'https://' + server + ":9443/v1/bdbs/" + id
   r = requests.delete(u, headers=headers, verify=False, auth=(user, password))
   return(r.status_code)

def list_databases(server, user, password):
   dbs = []
   headers = { 'Content-Type' : 'application/json'}
   u = 'https://' + server + ":9443/v1/bdbs"
   r = requests.get(u, headers=headers, verify=False, auth=(user, password))
   j = json.loads(r.text)
   for db in j:
      dbs.append({
         'name': db['name'],
         'port': db['port'],
         'size': db['memory_size']/(1024*1024*1024),
         'shards': db['shards_count'],
         'dbid': db['uid'],
         })

   return(dbs)


@app.route('/')
def index():
   return render_template('index.html')

@app.route('/show')
def showdbs():
   data = list_databases(redis_server, redis_user, redis_password)
   return render_template('show.html', results = data)

@app.route('/create')
def createdb():
   return render_template('index.html')

@app.route('/delete')
def deletedb():
   return render_template('delete.html')

@app.route('/whackdb', methods = ['POST'])
def whackdb():
   a = request.form.to_dict()
   resp = delete_database(redis_server, redis_user, redis_password, a['dbid'])
   return render_template('dbdeleted.html', db=a['dbid'], status = resp)

if __name__ == '__main__':
   bootstrap.init_app(app)
   nav.init_app(app)
   app.run()
