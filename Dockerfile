FROM python:alpine
RUN apk --no-cache add curl tzdata

RUN pip install --upgrade pip setuptools wheel && pip install Flask, psutil
COPY /app/ /app

ENTRYPOINT flask run --host=0.0.0.0