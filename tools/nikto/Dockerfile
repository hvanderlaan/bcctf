ARG ARCH=
FROM alpine:latest

LABEL version="v1.0.0" \
    author="Harald van der Laan <harald@familievdlaan.nl>"

RUN echo 'Installing Nikto requirements'
RUN apk add --update --no-cache --virtual .build-deps \
    git \
    perl \
    perl-net-ssleay

RUN echo 'Creating the nikto group.' \
    && addgroup nikto \
    && echo 'Creating the nikto user.' \
    && adduser -G nikto -g "Nikto user" -s /bin/sh -HD nikto

RUN echo 'Installing Nikto' \
    && git clone https://github.com/sullo/nikto /opt/nikto

ENV  PATH=${PATH}:/opt/nikto/program
USER nikto

ENTRYPOINT ["nikto.pl"]