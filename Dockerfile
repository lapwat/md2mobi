ARG PANDOC_VERSION=2.7

FROM ubuntu AS builder
ARG PANDOC_VERSION

RUN apt-get upgrade
RUN apt-get update && \
  apt-get install -y --no-install-recommends curl

ADD kindlegen_linux_2.6_i386_v2_9.tar.gz ./
RUN curl -kL https://github.com/jgm/pandoc/releases/download/${PANDOC_VERSION}/pandoc-${PANDOC_VERSION}-linux.tar.gz | tar xz

FROM python:alpine
ARG PANDOC_VERSION

RUN addgroup -S user && adduser -S user -G user

USER user
WORKDIR /home/user

COPY --from=builder pandoc-${PANDOC_VERSION}/bin/pandoc kindlegen /usr/local/bin/

# Python environment
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# scripts and static
COPY server.py convert.sh ./
COPY html html

EXPOSE 8000
ENTRYPOINT ["python", "server.py"]
