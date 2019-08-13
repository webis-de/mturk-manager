# MTurk Manager
This repository is intended to completely replace the requester site web page of Mechanical Turk.

The user is able to manage projects, upload batches, create different templates for better reviewing the results and many more.

The instructions can be found in the [Wiki](https://github.com/webis-de/mturk-manager/wiki) of this repository.  

The whole tool is built on top of [Vue.js](https://vuejs.org/) and the [Django-Framework](https://www.djangoproject.com/).  

## Requirements
* [Docker](https://docs.docker.com/)
* optional: [Docker Compose](https://docs.docker.com/compose/)

## Frontend
The frontend is needed to serve the UI of the MTurk Manager.

The frontend version has to match the backend version, otherwise unexpected behaviour may occur.

### Install/Run
Execute `docker run -d -p <port>:80 kritten/mturk-manager-frontend:1.5.2`

This will pull the image from [dockerhub](https://hub.docker.com/) and run the nginx server inside the container on the given port.


If you don't want to use docker, you have to manually serve the static files located in `frontend/dist` on a webserver of your choice.

## Backend
The backend server serves the MTurk Manager api which responses the requests coming from the frontend.
The whole backend consists of a django server, a postgres database, a rabbitmq instanace and a celery worker.

### Install/Run
1. Copy the following content into a `docker-compose.yml` file and replace `<port>` with an arbitrary port 
```
version: '3.7'

services:
  backend:
    image: kritten/mturk-manager-backend:${VERSION_MTURK_MANAGER}
    depends_on:
      - db
      - rabbitmq
    ports:
      - <port>:8000
    environment:
      - VERSION_MTURK_MANAGER=${VERSION_MTURK_MANAGER}
      - URL_GLOBAL_DB=${URL_GLOBAL_DB}
      - DATABASE_URL=${DATABASE_URL}

  db:
    image: postgres:10
    volumes:
      - type: bind
        source: ${PATH_DATABASE_DATA}
        target: /var/lib/postgresql/data/
    ports:
      - 5432:5432
    environment:
      - PATH_DATABASE_DATA=${PATH_DATABASE_DATA}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}

  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - 5672:5672

  celery:
    image: kritten/mturk-manager-backend:${VERSION_MTURK_MANAGER}
    command: /venv/bin/celery -A mturk_db worker -l info --concurrency=1
    depends_on:
      - rabbitmq
    environment:
      - C_FORCE_ROOT=true
      - VERSION_MTURK_MANAGER=${VERSION_MTURK_MANAGER}
      - URL_GLOBAL_DB=${URL_GLOBAL_DB}
      - DATABASE_URL=${DATABASE_URL}
```

2. Copy the following content in an `.env` file and fill the respective values
```
VERSION_MTURK_MANAGER=<version>
PATH_DATABASE_DATA=<absolute path>

DATABASE_URL=postgres://<postgres user>:<postgres password>@db:5432/<postgres database>
URL_GLOBAL_DB=<your domain (https!)>

POSTGRES_USER=<postgres user>
POSTGRES_PASSWORD=<postgres password>
POSTGRES_DB=<postgres database>
```

3. Execute `docker-compose up -d`

### Installation / Update
1. Execute `./setup_db.sh` to pull changes from the repository and install missing dependencies.
2. Execute `cd mturk`
3. Execute `python3 manage.py migrate`

**Only Once:**

1. Execute `python3 manage.py set_tokens <instance token> <worker token>`. The tokens can be arbitrary and are used by the frontend and mturk workers to authenticate with the database
2. Execute `python3 manage.py set_mturk_account <name> <access key> <secret key>`. The name is arbitrary and the keys are your [AWS security credentials](https://docs.aws.amazon.com/AWSMechTurk/latest/AWSMechanicalTurkGettingStartedGuide/SetUp.html).

### Startup Server
1. Run `cd mturk_db`
2. Run `python3 manage.py runserver 8001` to start the server _([more](https://docs.djangoproject.com/en/2.2/ref/django-admin/#django-admin-runserver) on how to start a django server)_

## Supported Features
* Create and manage mechanical turk projects
* Define **multiple** worker templates per project
* Customize the layout of the worker results
* Extensive approve/reject facility

## Contributors
* Kristof Komlossy
* Martin Potthast
* Matthias Hagen
* Florian Kneist

## Contact
Did you find a bug or do you have questions/requests?  
Write me a mail: mturk@kritten.org
