# Car Service API

## Table of contents
* [General info](#general-info)
* [Architecture](#architecture)
* [Installation](#installation)
* [API](#api)
* [Tests](#tests)
* [Checklist](#checklist)

## General info

This project is a solution to Distilled SCH coding challange. The challange required the system to expose RESTFull apis, and serve those apis while interfacing with the database (sqlite) with the appropriate implementation of testing, stability, security and maintainability of the system. The challange requires the implementation to

1. be in Python 3.x
2. exposes Endpoint to retrieve a record by id without chassis number.
3. exposes Endpoint to return the average price by  make  or  model  or  year, or their combinations
5. includes DDL and DML to create the database and table and load from csv above.

with extra functionalities such as:

1. implementation of swagger endpoint to describe and document the API.
2. Dockerization of the system
3. Dockerization of the web service and database using docker compose.


## Architecture

This project address all those functionalities mentioned in the previous section. 
On a highest level, The system is implemented inside the docker container while utilizing the WSGI (gunicorn), python micro-framework (flask), object relational mapper like SQLAlchemy and along with realted utilities as shown in the architecture.png


![Architecture](architecture.jpg)

Certain considerations are carried out in the implementation of the ORM and db queries. All the db queries were made from a separate file, called dbhandler.py, to retrieve and send the data to and from database. This potentially raise some circular referencing issues in the code but reinforce the modularity and clarity of the codebase.   

## Installation

To run this project, docker and docker compose installation is required. Which can be found at https://docs.docker.com/install/.
Further installation is done within the docker and required no manual installation:


### Clone

- Clone this repo to your local machine using 

`git clone https://github.com/ebadali/distilled_challange.git`

### Setup


- Build and run docker files using docker compose

```shell
$ docker compose -up --build
```



## APIs

RESTFull apis are implemented using the Flask micro-framework to enable other applications to utilize the car-service resources on HTTP protocol in a stateless fashion.  


All API responses will have the form

```json
{
    "data": "Mixed type holding the content of the response",
    "status": "Description of what happened as in 'success' or 'failure'"
}
```

Subsequent response definitions will only detail the expected value of the `data field`

### Authentication

Access to the API is granted by providing an Access token in the HTTP Authroziation header. This authentation is simulated by hardcoding a key phrase ```Some_Predefined_Token``` in the authorization header along with bearer in the form of 

```
curl -H "Authorization: Bearer Some_Predefined_Token" https://some.resource
```



### List all Cars

**Definition**

`GET /cars`

**Response**

- `200 OK` on success

```json
[
    {
      "identifier": 1,
      "last_updated": "2017-02-01 00:00:00",
      "make": "Nissan",
      "model": "Micra",
      "price": "500.0",
      "year": "2004"
    }
]
```

**Example**

```
curl -H "Authorization: Bearer Some_Predefined_Tokena" http://0.0.0.0:5000/cars
```

### Lookup car details

`GET /car/<identifier>`

**Arguments**

- `"identifier":string` an identifier for this car. Not neccesasrily unique

**Response**

- `404 Not Found` if the car does not exist
- `200 OK` on success

```json
{
    "data" : {
      "identifier": 1,
      "last_updated": "2017-02-01 00:00:00",
      "make": "Nissan",
      "model": "Micra",
      "price": "500.0",
      "year": "2004"
    }
}
```
**Example**

```
curl -H "Authorization: Bearer Some_Predefined_Tokena" http://0.0.0.0:5000/car/2
```

### Calculate average price by make and/or model and/or year

`GET /car/aggregator/price`

`GET /car/aggregator/price?make=<make>&model=<model>&year=<year>`

**Querystring Arguments (optional)**

- `"make":string` make of the car such as : Nissan
- `"model":string` model such as : Micra
- `"year":string` model year of the car such as : 2002


**Response**

- `404 Not Found` if the device does not exist
- `200 OK` on success

```json
{
    "data" : 234.53
}
```

**Example**

```
curl -H "Authorization: Bearer Some_Predefined_Tokena" http://0.0.0.0:5000/car/aggregator/price?make=Nissan&model=Micra&year=2002
```


## Tests
Testing of the endpoints are performed using python's unittest module. The idea is to test all the endpoints with all the use-cases. In this tests directory, however, not all the use-cases are captured and required further implementation of integration and unit tests. All the tests are located in the ```tests``` directory. In order to run all the tests, in the root directory of the project run 

```
nosetests --verbose
```


## Checklist


**Required**

- [x] Python 3.x usage
- [x] Endpoint to retrieve a record by id excluding the ‘chassis_no` 
- [x] OEndpoint to return the average price by  make  or  model  or  year,   or a combination of the

**Extras**

- [x] implementation of swagger endpoint at : http://0.0.0.0:5000/swagger
- [x] Dockerization of the system
- [ ] Dockerization of the web service and database using docker compose: This however is implemented in a separate docker compose file called 'docker-compose-postgress.yaml' which, instead of sqlite, dockerize the postgress and python app in a separate containers and uses docker compose to run it.