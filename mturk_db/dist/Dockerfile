FROM phusion/baseimage:0.11

WORKDIR /app

ADD . /app
#
#RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
#RUN apt-get install -y python3.6
#RUN update-alternatives --install /usr/bin/python3 python /usr/bin/python3.6 2


# To prevent timezone info prompt during postgresql installation
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
RUN apt-get install -y --no-install-recommends git python3-pip postgresql postgresql-contrib nano apache2 apache2-dev python3-psycopg2 libapache2-mod-wsgi-py3
RUN pip3 install psycopg2 django==2.0 boto3 xmltodict djangorestframework markdown requests

#RUN apt-get install -y --no-install-recommends git python3-pip python3.6-dev postgresql postgresql-contrib nano apache2 apache2-dev python3-psycopg2 libpq-dev
##RUN apt-get install -y --no-install-recommends git python3-pip postgresql postgresql-contrib nano apache2 libapache2-mod-wsgi-py3 python3-psycopg2 libpq-dev
#RUN pip3 install --upgrade pip
#RUN pip3 install --upgrade setuptools
#RUN pip3 install mod_wsgi psycopg2-binary django==2.0 boto3 xmltodict djangorestframework markdown requests
#RUN pip3 install psycopg2 django==2.0 boto3 xmltodict djangorestframework markdown requests
#RUN a2enmod wsgi
#
WORKDIR /var/www/python
RUN git clone https://github.com/webis-de/mturk-manager.git
#
ARG setting_files=/kritten
ENV folder_setting_files=$setting_files
#
EXPOSE 8000
EXPOSE 80
#
WORKDIR /app
CMD ["python3", "app.py"]
#CMD ["python3"]