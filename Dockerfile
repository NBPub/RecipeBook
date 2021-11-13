FROM python:alpine

ENV TZ=America/Los_Angeles

RUN apk --no-cache add curl tzdata

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY /app/ .

ENTRYPOINT FLASK_APP=RecipeReader.py flask run --host=0.0.0.0

EXPOSE 5000

VOLUME /recipes