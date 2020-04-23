# Self Serve Enterprise Portal Example

This is an example of how to create a self serve portal for users within your organization on Redis Enterprise.

Users can create, delete and view Redis databases on an Enterprise cluster.


## Running with Docker

### Prerequisites 
- [Docker](https://www.docker.com/products/docker-desktop)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Running Dockerized Version

```
git clone https://github.com/Redislabs-Solution-Architects/SelfServeEnterprise.git
cd SelfServeEnterprise
cp docker-compose.yml.example docker-compose.yml

# Edit the file to add your credentials

docker-compose up
```

[Open This Link in Your Browser](http://localhost:5000)


## Running Locally


### Install python requirements

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Start the flask app

```
# Set credentials as enviornment variables

export REDIS_SERVER=mycluster.example.com
export REDIS_USER=redisadmin@example.com
export REDIS_PASSWORD=myPassword1234

# start application
python3 app.py 
```

### Navigate to the home page

1) [Webapp](http://localhost:5000)

