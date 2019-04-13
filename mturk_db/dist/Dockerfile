FROM phusion/baseimage:0.9.19

WORKDIR /app

ADD . /app

RUN apt-get update && apt-get install -y --no-install-recommends python3.5 git python3-pip postgresql postgresql-contrib nano apache2 libapache2-mod-wsgi-py3 python3-psycopg2 libpq-dev
RUN a2enmod wsgi
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install psycopg2 django==2.0 boto3 xmltodict djangorestframework markdown requests

WORKDIR /var/www/python
RUN git clone https://github.com/webis-de/mturk-manager.git

ARG setting_files=/kritten
ENV folder_setting_files=$setting_files

EXPOSE 8000
EXPOSE 80

WORKDIR /app
CMD ["python3", "app.py"]