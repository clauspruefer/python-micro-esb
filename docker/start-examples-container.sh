#!/bin/sh

docker run --name microesb-postgres \
-d -p 5432:5432 \
--add-host=localdb:127.0.0.1 \
microesb-examples:latest postgres

