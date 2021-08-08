FROM python:3.9.5-slim-buster

WORKDIR /home/myproj

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY main.py ./
COPY worker.py ./