# Trips Ingestion
Code created to ingest CSV file with trips to PostgreSQL, process table and 
create views.

## Tecnologies
- Python 3.8
- Postgres
- Docker composer

### Poetry
[Poetry](https://python-poetry.org/) is a Python tool for packaging and dependency management.

### Dynaconf
[Dynaconf](https://www.dynaconf.com/) is a python lib to get environment var.
In this code, var are stored in a file called .secrets.toml. Dynaconf will load var from this file.

## Get Started
### Requisites
Install docker:
- [Windows](https://docs.docker.com/desktop/windows/)
- [OS X](https://docs.docker.com/desktop/mac/)
- [Linux](https://docs.docker.com/engine/install/)

### Clone repo and up containers
```commandline
git clone https://github.com/LeonardoGazziro/trips-ingestion.git
cd trips-ingestion
docker-compose up
```

### Access pgAdmin
* http://localhost:16543
* Login on pgAdmin4 page: postgres@gmail.com
* Password on pgAdmin4 page: postgres
* Add a new server using:
  * Hostname: postgis
  * User:postgres
  * Password:!2qwaszx

### Process CSV file:
This command will start the ingestion process. 
```commandline
docker exec -it python poetry run trips
```

## Features
* Automate process to read csv and save in Postgres, using Python, Pandas and SQLAlchemy.
* Create a view to get similar trips (2.5 kilometers radius) from origin, destination and hour of day
* Create view to get the weekly average trips by region 
* After process file it will be moved to a folder called "processed"

## Scalability
### Create CSV file
To create CSV with 50mi rows use the python code in /other/create_csv.py.
```commandline
docker exec -it python poetry run create_50mi_file
```

### Tests
This code can be used with 100mi rows or more, my test have 50mi.
#### Results:
![50mi-rows](/others/imgs/50mi-test.png) 

Test machine:
CPU: i7-9750H 2.6
RAM: 16 GB
DISK: SSD M2 128 MB
O.S.: Linux Mint 19

## Process description
When Python script trips is called, it will load CSV file (/input_files) using 
Pandas in chunks of 5000000 row, and save in Postgres in chunks of 10000 row.
The chunk size can be changed on .secrets.toml file.

After reading and inserting data in Postgres the file will be coped to a folder called processed.

The next step is to execute the SQL script file (/SQL/create_trips_log.sql), this sql will create
a table in schema called operation, insert typed rows and create two views for 
similar trips and weekly trips.

## GCP sketch
![GCP](/others/imgs/gcp-sketch.png) 