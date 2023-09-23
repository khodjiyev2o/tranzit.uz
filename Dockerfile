FROM python:3.9.2-alpine


# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add libffi-dev postgresql-dev wkhtmltopdf gcc python3-dev musl-dev py-pip jpeg-dev zlib-dev \
    && apk add libressl-dev perl rust libmagic pango openjpeg-dev g++

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements/base.txt .
COPY ./requirements/prod.txt .

RUN pip install -r prod.txt

# copy entrypoint.sh
COPY entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
