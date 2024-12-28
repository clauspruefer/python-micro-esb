FROM postgres:latest
MAINTAINER Claus Prüfer

ADD ./example /
COPY ./dist/microesb-1.0rc1.tar.gz /

COPY ./example/01-hosting-use-case/01-create-schema-sequence.sql /docker-entrypoint-initdb.d/
COPY ./example/01-hosting-use-case/02-create-table.sql /docker-entrypoint-initdb.d/
COPY ./example/01-hosting-use-case/03-create-index.sql /docker-entrypoint-initdb.d/
COPY ./example/01-hosting-use-case/04-insert-user-data.sql /docker-entrypoint-initdb.d/

RUN apt-get -qq update -y

RUN apt-get -qq install python3-pip python3-sphinx python3-sphinx-rtd-theme -y
RUN apt-get -qq install python3-pytest python3-pytest-pep8 -y
RUN apt-get -qq install python3-psycopg2 -y

RUN pip3 install /microesb-1.0rc1.tar.gz --break-system-packages

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD password
ENV POSTGRES_DB hosting-example

EXPOSE 5432

