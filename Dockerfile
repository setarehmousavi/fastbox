FROM python:3.13-bullseye

ENV PYTHONUNBUFFERED=1
ENV DJANGO_CONFIGURATION=Docker
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && apt-get install -y gcc ghostscript
RUN pip install --upgrade pip

RUN mkdir /fastbox
WORKDIR /fastbox
ADD /fastbox/requirements.txt /fastbox

RUN pip install -r requirements.txt

ADD ./fastbox /fastbox