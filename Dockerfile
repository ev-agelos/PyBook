FROM python:3.8-slim-buster

COPY ./requirements/prod.txt /tmp/requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
	&& rm -rf /var/lib/apt/lists/*

RUN pip install -r /tmp/requirements.txt && mkdir -p /var/lib/sqlite3/data

ADD . /PyBook

WORKDIR /PyBook

CMD gunicorn --bind :9000 --workers=2 wsgi:app
