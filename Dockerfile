FROM python:3.8.3-alpine as builder

COPY ./requirements/prod.txt /tmp/requirements.txt

RUN apk add --update gcc libffi-dev musl-dev \
    && pip wheel -r /tmp/requirements.txt --wheel-dir=/root/wheels

FROM python:3.8.3-alpine
COPY --from=builder /root/wheels/ /root/wheels/
COPY --from=builder /tmp/requirements.txt /tmp/requirements.txt

RUN pip install --no-index --find-links=/root/wheels -r /tmp/requirements.txt \
    && rm -rf /root/wheels

RUN mkdir -p /var/lib/sqlite3/data

ADD . /app
WORKDIR /app

CMD gunicorn --bind :9000 --workers=2 wsgi:app
