FROM ubuntu:xenial 

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y apt-utils

RUN apt-get install -y \
    build-essential \
    python3-pip

ENV DEBIAN_FRONTEND=teletype

WORKDIR /src
COPY . /src

RUN pip3 install -r requirements.pip

EXPOSE 5000

