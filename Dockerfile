FROM python:3.7-alpine
RUN ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime
RUN echo "http://mirror.leaseweb.com/alpine/edge/testing" >> /etc/apk/repositories
RUN apk update && apk upgrade
RUN apk add --no-cache gcc libc-dev linux-headers bash python3-dev libgcc libstdc++ musl geos-dev libxml2-dev libxslt-dev
COPY . /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r requirements.txt
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0 --workers=2 --threads=1 --log-level=debug"
CMD ["gunicorn", "wsgi:app"]