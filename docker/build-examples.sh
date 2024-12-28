#!/bin/sh

workdir="$(echo $PWD)"

cd ../

# build module source distribution
python3 setup.py sdist

# build docker container
docker build -t microesb-examples --file ./docker/examples.dockerfile .

cd ${workdir}

