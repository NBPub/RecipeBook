FROM python:slim-bullseye

RUN apt-get update && \
    apt-get upgrade -y && \
	apt-get install gcc python3-dev  -y --no-install-recommends

RUN pip install --upgrade pip setuptools wheel && pip install Flask psutil
COPY /app/ /app

ENTRYPOINT flask run --host=0.0.0.0