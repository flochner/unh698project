FROM ubuntu:xenial 

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y apt-utils

RUN apt-get install -y \
    build-essential \
    python3-pip

RUN pip3 install flask prometheus_client

ENV DEBIAN_FRONTEND=teletype

WORKDIR /src
COPY . /src

EXPOSE 5000
