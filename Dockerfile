FROM python:3.7-alpine

LABEL version="1.0"
LABEL maintainer="Sergey Kushnerchuk"

WORKDIR /app

COPY requirements.txt /app
RUN echo "http://mirror.leaseweb.com/alpine/edge/testing" >> /etc/apk/repositories \
    && apk update \
    && apk add --no-cache --virtual .build-deps gcc libc-dev linux-headers bash \
            python3-dev libgcc libstdc++ musl geos-dev libxml2-dev libxslt-dev \
            mariadb-dev libffi libffi-dev gmp-dev mpfr-dev bash jq curl \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del --no-cache --purge .build-deps \
    && rm -rf /var/cache/apk/*

RUN apk add --no-cache mariadb-dev && rm -rf /var/cache/apk/*

COPY . /app
WORKDIR /app


ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0 --workers=2 --threads=1 --log-level=debug -c gunicorn_conf.py"

ENTRYPOINT ["gunicorn", "wsgi:app"]
