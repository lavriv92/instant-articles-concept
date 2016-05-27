FROM python:3.5

ENV PYTHONBUFFERED 1

RUN mkdir /app

WORKDIR /app

RUN apt-get install -y gcc

ADD requirements.txt /app/

RUN pip install -r requirements.txt

ADD . /app/
