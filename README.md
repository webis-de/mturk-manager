# MTurk Manager
This repository is intended to completely replace the requester site web page of Mechanical Turk.

The user is able to manage projects, upload batches, create different templates for better reviewing the results and many more.

The instructions can be found in the [Wiki](https://github.com/webis-de/mturk-manager/wiki) of this repository.  

The whole tool is built on top of [Vue.js](https://vuejs.org/) and the [Django-Framework](https://www.djangoproject.com/).  

## Requirements
* [Docker](https://docs.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)

## Frontend
The frontend is needed to serve the UI of the MTurk Manager.

The frontend version has to match the backend version, otherwise unexpected behaviour may occur.

## Backend
The backend server serves the MTurk Manager api which responses to requests coming from the frontend.

The whole backend consists of a django server, a postgres database, a rabbitmq instanace and a celery worker.

## Run
You don't need to pull this repository, you only need `scripts/docker-compose.yml` and `scripts/.env`

1. Adjust the values in `.env` to your need. *Don't forget to add the data path for the database (`PATH_DATABASE_DATA`) and ensure the path exists*
2. Run `docker-compose up -d` to start the back- and frontend
3. Run `docker exec mturk-manager-backend-<version> /code/setup.sh` to initialize the database

Run the last command (at 3.) every time you update the version of the mturk manager and/or you change the `INSTANCE_TOKEN` and `WORKER_TOKEN` in `.env`.

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
