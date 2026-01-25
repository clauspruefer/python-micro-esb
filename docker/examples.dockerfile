FROM postgres:18-bookworm
MAINTAINER Claus Prüfer

ADD ./example /
COPY ./dist/microesb-1.1.1.tar.gz /

COPY ./example/01-hosting-use-case/01-create-schema-sequence.sql /docker-entrypoint-initdb.d/
COPY ./example/01-hosting-use-case/02-create-table.sql /docker-entrypoint-initdb.d/
COPY ./example/01-hosting-use-case/03-create-index.sql /docker-entrypoint-initdb.d/
COPY ./example/01-hosting-use-case/04-insert-user-data.sql /docker-entrypoint-initdb.d/

RUN apt-get -qq update -y

RUN apt-get -qq install python3-pip -y
RUN apt-get -qq install python3-psycopg2 python3-pymongo -y
RUN apt-get -qq install curl -y

RUN curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg --dearmor

RUN echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/debian bookworm/mongodb-org/8.0 main" | tee /etc/apt/sources.list.d/mongodb-org-8.0.list

RUN apt-get -qq update
RUN apt-get -qq install mongodb-org -y

RUN mkdir -p /data/db

RUN pip3 install /microesb-1.1.1.tar.gz --break-system-packages

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD password
ENV POSTGRES_DB hosting-example

EXPOSE 5432
