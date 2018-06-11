# MTurk Manager
This repository houses a web server which is able to completely replace the requester site web page of Mechanical Turk.

The user is able to manage projects, upload batches, create different templates for better reviewing the results and many more.

The instructions of how to write that file can be found in the [Wiki](https://github.com/webis-de/mturk-manager/wiki) of this repository.  

The whole tool is built on top of the [Django-Framework](https://www.djangoproject.com/).  

## Requirements
* Python 3.5+

## Installation
**Note:** If you want to use a virtual environment like `virtualenv` switch to the virtual environment before executing the following step(s)!

1. Run `./setup.sh`

## Quickstart
1. Run `cd mturk`
2. Run `python3 manage.py runserver` to start the server _([more](https://docs.djangoproject.com/en/2.0/ref/django-admin/#django-admin-runserver) on how to start a django server)_
3. Visit [localhost:8000](http://localhost:8000)

## Update
**Note:** It's a good idea to backup your database _(`mturk/db.sqlite3`)_ before executing the following steps!

1. Stop the server
2. Run `cd ../`
3. Run `./setup.sh` _(this will also pull the most recent changes)_
4. Run `cd mturk` 
5. Run `python3 manage.py runserver` to start the server _([more](https://docs.djangoproject.com/en/2.0/ref/django-admin/#django-admin-runserver) on how to start a django server)_

## Supported Features
* Create and manage mechanical turk projects
* Define **multiple** worker templates per project
* Customize the layout of the worker results
* Extensive approve/reject facility

## Upcoming Features
* Filter and download the hit results as json or csv

## Contributors
* Kristof Komlossy
* Martin Potthast
* Matthias Hagen

## Contact
Did you find a bug or do you have questions/requests?  
Write me a mail: kristof.komlossy@uni-weimar.de
