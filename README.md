# Dockerised Data Processing Pipeline


## What we are going to do

For this project we are going to use Docker Compose to glue together a basic Realtime Data Processing Pipeline using free and OpenSource software. 

It's the supporting repository for a presentation I made in July 2019, for a (self hosted) dockerisation of the work done in Spring 2019 by Sahil Dadia in a series of workshops presented at the Data Science and Engineering Club, a friendly and (very!) hands-on meetup organised by Roman Golovnya in Dublin.


## What's the tech stack

The only two requirements to follow along are:

- Docker
- Docker Compose

We'll pull from Docker Hub the following tools, which are not required to be installed in the developer machine, as they will all be used within dedicated containers:

- Python
- [Kafka](https://hub.docker.com/r/wurstmeister/kafka/)
- PostgreSQL
- [Apache Superset](https://hub.docker.com/r/amancevice/superset/)


## How to start the services

Go into the root of the project and start a single node Kafka cluster (with supporting Zookeper instance) and a PostgreSQL server:

```sh
docker-compose up -d kafka postgres
```

You can see if the 3 service (`zookeeper`, `kafka` and `postgres`) and up and running with the following command:

```sh
docker ps --format "{{.Image}}  {{.Status}}"
```

It should give an output similar to this:

```sh
wurstmeister/kafka:2.12-2.2.1  Up 3 minutes
wurstmeister/zookeeper  Up 3 minutes
postgres:11.2  Up 3 minutes
```

When Postgres is up and running, you can setup a local Apache Superset instance, running the following command (only needed the first time: the postgres data is persisted in the local folder `data/postgres/pgdata`). Run the following two commands:

```sh
docker-compose run superset superset-init
```

You will be asked a few questions:

```text
Username [admin]:
User first name [admin]:
User last name [user]:
Email [admin@fab.org]:
Password:
Repeat for confirmation:
```

Just press the **[RETURN]** key to accept the defaul value for the first four questions, and pick a password for your admin user in the last two.

You'll get a few more messages from the init script while the database is created and setup.

Now you can start the Superset service:

```sh
docker-compose up -d superset
```

_(NOTE: see my [Dockerised Superset](https://github.com/enricomarchesin/dockerised-superset) repo for further customisation options...)_

All going fine you can run the `docker ps` command again:

```sh
docker ps --format "{{.Image}}  {{.Status}}"
```

You now should have two more services running, `superset` and `redis`:

```sh
amancevice/superset:0.28.1: Up 3 seconds (health: starting)
wurstmeister/kafka:2.12-2.2.1: Up 32 minutes
wurstmeister/zookeeper: Up 32 minutes
redis: Up 4 seconds
postgres:11.2: Up 32 minutes
```


## Generate some random data

To create some fake data run:

```sh
docker-compose run producer
```

This will generate 10 random data records and send the to the Kafka cluster. You can run it a few times if you want more fake records to be generated.


## Consume the data

You are now ready to start reading from the ingestion queue the data you just submitted. Run the following:

```sh
docker-compose run consumer
```

This will pop the JSON messages in the Kafka cluster and store them in the Postgres database.


## Visualise the data

The Superset UI can be accessed at the following address:

> http://localhost:8088/

Log in with the username and password chosen in the initialisation step.

_TO BE CONTINUED (crate superset table, configure fields, create graph, create dashboard).


## When you are done

To tear down all the services, just run:

```sh
docker-compose down
```

Data in Kafka cluster nodes is deleted when cluter nodes are shutdown.

PostgreSQL data is persisted in the local folder `data/postgres/pgdata`: delete this folder if want to start from scratch.


## TODO

- [ ] complete visualisation section of tutorial
- [ ] polish python code
- [ ] kafka producer and consumer in other languages
