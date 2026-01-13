ARG ARCH=
FROM alpine:latest

LABEL version="v1.0.0" \
    author="Harald van der Laan <harald@familievdlaan.nl>"

RUN echo 'Installing john'
RUN apk add --update --no-cache --virtual .build-deps \
    john

RUN echo 'Creating the John group.' \
    && addgroup john \
    && echo 'Creating the John user.' \
    && adduser -G john -g "John the Ripper user" -s /bin/sh -HD john \
    && mkdir /home/john/ \
    && chown john:john /home/john

USER john

CMD ["john"]
