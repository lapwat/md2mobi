ARG PANDOC_VERSION=2.7

FROM ubuntu AS builder
ARG PANDOC_VERSION

RUN apt-get upgrade
RUN apt-get update && \
  apt-get install -y --no-install-recommends curl

RUN curl -kL https://github.com/jgm/pandoc/releases/download/${PANDOC_VERSION}/pandoc-${PANDOC_VERSION}-linux.tar.gz | tar xz
RUN curl http://kindlegen.s3.amazonaws.com/kindlegen_linux_2.6_i386_v2_9.tar.gz | tar xz

FROM python:alpine
ARG PANDOC_VERSION

RUN addgroup -S user && adduser -S user -G user

USER user
WORKDIR /home/user

COPY --from=builder pandoc-${PANDOC_VERSION}/bin/pandoc kindlegen /usr/local/bin/
COPY html html
COPY server.py convert.sh requirements.txt ./

RUN pip install --user -r requirements.txt
ENTRYPOINT ["python", "server.py"]
