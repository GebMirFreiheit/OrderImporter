FROM python:3.8

ARG POSTGRES_DB
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD

ENV POSTGRES_DB ${POSTGRES_DB?dbnamenotset}
ENV POSTGRES_USER ${POSTGRES_USER?dbusernotset}
ENV POSTGRES_PASSWORD ${POSTGRES_PASSWORD?dbpasswordnotset}
ENV PYTHONUNBUFFERED 1
RUN mkdir /web_django
WORKDIR /web_django
COPY requirements.txt /web_django/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /web_django/ 
