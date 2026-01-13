
ARG ARCH=
FROM alpine:latest
LABEL maintainer="Harald van der Laan <harald.vanderlaan@brightcubes.nl>"
LABEL description="Alpine based image with apache2 and php8 and vulnerable website"
LABEL version="v1.0.0"

# Setup apache and php
RUN apk --no-cache --update \
    add apache2 \
    apache2-ssl \
    bash \
    curl \
    php84-apache2 \
    php84-bcmath \
    php84-bz2 \
    php84-calendar \
    php84-common \
    php84-ctype \
    php84-curl \
    php84-dom \
    php84-gd \
    php84-iconv \
    php84-mbstring \
    php84-mysqli \
    php84-mysqlnd \
    php84-openssl \
    php84-pdo_mysql \
    php84-pdo_pgsql \
    php84-pdo_sqlite \
    php84-phar \
    php84-session \
    php84-xml \
    python3 \
    socat \
    sudo \
    && mkdir -p /htdocs/uploads \
    && chown apache:apache /htdocs/uploads

EXPOSE 80 443

ADD docker-entrypoint.sh /
ADD rootflag.txt /flag.txt
ADD userflag.txt /htdocs/flag.txt
ADD index.html /htdocs/index.html
ADD upload.php /htdocs/upload.php

HEALTHCHECK CMD wget -q --no-cache --spider localhost

ENTRYPOINT ["/docker-entrypoint.sh"]
