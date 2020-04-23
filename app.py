from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from os import environ

import json
import requests
import random
import string

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

def randomString(stringLength=8):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

def create_database(server, user, password, params, port, passwd):
   headers = { 'Content-Type' : 'application/json'}
   if int(params['dbshards']) > 1 :
      s = True
   else:
      s = False
   u = 'https://' + server + ":9443/v1/bdbs"
   r = requests.post(
        u,
        headers=headers,
        verify=False,
        timeout=60,
        auth=(user, password),
        json={
           "name": params['dbname'],
           "memory_size": int(params['dbsize'])*1024*1024*1024,
           "type": "redis",
           "shard_key_regex": [{'regex': '.*\\{(?<tag>.*)\\}.*'}, {'regex': '(?<tag>.*)'}],
           "sharding": s,
           "port": port,
           "shards_count": int(params['dbshards']),
           "authentication_redis_pass": passwd }
        )
   j = json.loads(r.text)
   return(j)

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
   return render_template('create.html')

@app.route('/delete')
def deletedb():
   return render_template('delete.html')

@app.route('/dbcreate', methods = ['POST'])
def dbcreate():
   used_ports=list(map(lambda x: x['port'] , list_databases(redis_server, redis_user, redis_password)))
   for i in range(10001, 19999):
      if i in used_ports:
         continue
      else:
         rport=i
      break
   a = request.form.to_dict()
   resp = create_database(redis_server, redis_user, redis_password, a, rport, randomString(16))
   return render_template('dbcreated.html', db=a['dbname'], status = resp)


@app.route('/whackdb', methods = ['POST'])
def whackdb():
   a = request.form.to_dict()
   resp = delete_database(redis_server, redis_user, redis_password, a['dbid'])
   return render_template('dbdeleted.html', db=a['dbid'], status = resp)

if __name__ == '__main__':
   bootstrap.init_app(app)
   nav.init_app(app)
   app.run()
