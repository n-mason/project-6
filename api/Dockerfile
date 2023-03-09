FROM python:3.8
MAINTAINER Nathaniel Mason "nmason@uoregon.edu"
RUN apt-get update -y
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt