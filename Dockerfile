FROM python:alpine
RUN apk --no-cache add curl tzdata
WORKDIR /app

RUN pip install --upgrade pip setuptools wheel && pip install Flask
COPY /app/ .

ENTRYPOINT flask run --host=0.0.0.0