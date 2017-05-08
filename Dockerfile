FROM ubuntu:xenial 

RUN apt-get update

RUN apt-get install -y apt-utils

RUN apt-get install -y \
    build-essential \
    python3-pip

RUN pip3 install flask prometheus_client

WORKDIR /src
COPY . /src

EXPOSE 5000
