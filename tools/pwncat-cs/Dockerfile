FROM python:3.10-slim

RUN apt update \
    && apt install -y build-essential \
    && pip install --upgrade pip setuptools \
    && pip install pwncat-cs \
    && mkdir /work

WORKDIR /work

ENTRYPOINT ["pwncat-cs"]