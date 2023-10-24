# pull official base image
FROM python:3.9.2-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1


# install psycopg2 dependencies
RUN apk update \
    && apk add libffi-dev postgresql-dev gcc python3-dev py-pip jpeg-dev zlib-dev \

RUN apk --no-cache add \
    icu-dev \


RUN apk --no-cache add glib-dev poppler-glib vips-dev vips-tools poppler-utils

COPY requirements/ .

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r production.txt

# create directory for the app user
RUN mkdir -p /home/app

# create the app user

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
RUN mkdir $APP_HOME/locale
WORKDIR $APP_HOME

# copy entrypoint.sh
COPY ./entrypoint.sh $APP_HOME

# copy project
COPY . $APP_HOME


# run entrypoint.prod.sh
RUN ["chmod", "+x", "/home/app/web/entrypoint.sh"]
ENTRYPOINT ["/home/app/web/entrypoint.sh"]

