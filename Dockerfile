FROM alpine:3.8
RUN \
    apk add --no-cache -v postgresql python3 less groff \
    && pip3 install awscli \
    && mkdir -p /out
COPY script.py /app/
WORKDIR /app
VOLUME ["/out"]
ENTRYPOINT ["python3", "script.py"]
