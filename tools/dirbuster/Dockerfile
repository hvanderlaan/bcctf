ARG ARCH=
FROM alpine:latest

LABEL maintainer="Harald van der Laan <harald.vanderlaan@brightcube.nl"
LABEL version="v1.0.2."

RUN apk add python3 py3-virtualenv\
    && mkdir /app

WORKDIR /app

RUN python3 -m venv .venv \
    && source .venv/bin/activate \
    && pip install --upgrade pip \
    && pip install colorama requests tqdm

ADD src/ /app/

ENTRYPOINT [ "/app/docker-entrypoint.sh" ]
