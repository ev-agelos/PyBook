FROM python:3.7-alpine

# Hotfix for glibc hack that fixes the order of DNS resolving (i.e. check /etc/hosts first and then lookup DNS-servers).
# To fix this we just create /etc/nsswitch.conf and add the following line:
ONBUILD RUN echo 'hosts: files mdns4_minimal [NOTFOUND=return] dns mdns4' >> /etc/nsswitch.conf

COPY ./requirements/prod.txt /tmp/requirements.txt

RUN apk add --update gcc libffi-dev musl-dev && \
    rm /var/cache/apk/* && \
    pip install setuptools --upgrade && pip install -r /tmp/requirements.txt && \
    apk del --purge gcc musl-dev && \
    mkdir -p /var/lib/sqlite3/data

ADD . /PyBook

WORKDIR /PyBook

CMD gunicorn --bind :9000 --workers=2 wsgi:app
