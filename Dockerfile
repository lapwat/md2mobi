FROM ubuntu

RUN apt-get upgrade
RUN apt-get update && \
  apt-get install -y --no-install-recommends curl pandoc

RUN curl http://kindlegen.s3.amazonaws.com/kindlegen_linux_2.6_i386_v2_9.tar.gz -o kindlegen.tar.gz
RUN tar xzf kindlegen.tar.gz

COPY entrypoint.sh .

ENTRYPOINT ["./entrypoint.sh"]
