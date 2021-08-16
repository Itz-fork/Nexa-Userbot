FROM ubuntu:latest
WORKDIR .
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    python3 \
    megatools
RUN pip3 install -r requirements.txt
RUN bash startup.sh
