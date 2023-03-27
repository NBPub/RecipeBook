# build stage

FROM python:slim-bullseye as builder

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get upgrade -y && \
	apt-get install -y --no-install-recommends gcc python3-dev
	
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /code/wheels -r requirements.txt

# final

FROM python:slim-bullseye

WORKDIR /code

COPY --from=builder /code/wheels /wheels
COPY --from=builder /code/requirements.txt .

RUN pip install --no-cache /wheels/*

COPY /app/ ./app

ENTRYPOINT flask run --host=0.0.0.0