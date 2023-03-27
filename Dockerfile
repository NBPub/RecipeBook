FROM python:alpine

RUN apk --no-cache add curl tzdata gcc python3-dev

RUN pip install --upgrade pip setuptools wheel && pip install Flask && pip install --no-binary :all: psutil

COPY /app/ /app

ENTRYPOINT flask run --host=0.0.0.0