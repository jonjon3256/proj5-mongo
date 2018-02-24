FROM python:3
Maintainer Jonathan Rodriguez "jrodrig2@uoregon.edu"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
ADD . /todo
WORKDIR /todo
RUN pip install -r requirements.txt
