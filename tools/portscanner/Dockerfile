FROM alpine:latest

LABEL maintainer="Harald van der Laan" \
      version="v0.1.1"

RUN apk add python3 py3-virtualenv \
    && mkdir /app \
    && cd /app

WORKDIR /app

ADD ./portscanner.py portscanner.py
ADD ./requirements.txt requirements.txt
ADD ./docker-entrypoint.sh docker-entrypoint.sh

RUN python3 -m venv .venv \
    && source .venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

ENTRYPOINT [ "./docker-entrypoint.sh" ]