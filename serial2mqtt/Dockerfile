ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

RUN apk add --no-cache python3 && \
    python3 -m ensurepip --upgrade && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools crcmod paho-mqtt pyserial && \
    rm -r /root/.cache

# Python 3 HTTP Server serves the current working dir
# So let's set it to our add-on persistent data directory.
WORKDIR /data

COPY main.py /
COPY run.sh /
RUN chmod a+x /main.py
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
