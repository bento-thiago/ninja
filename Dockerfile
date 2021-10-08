FROM nasajon/django:latest
LABEL maintainer="DevOps <devops@nasajon.com.br>"

COPY requirements.txt /var/www/html

RUN apk update
RUN apk --update add tzdata
RUN apk add --no-cache mariadb-dev

RUN python3 -m pip install -r /var/www/html/requirements.txt --no-cache-dir

RUN echo "America/Sao_Paulo" >  /etc/timezone

RUN mkdir /var/app_home

RUN chmod 777 /var/app_home

COPY . /var/www/html

ENV PYTHONPATH=/var/www/html