FROM debian:latest

RUN apt update && apt upgrade -y
RUN apt install git curl python3-pip ffmpeg -y
RUN apt -qq install -y --no-install-recommends megatools
RUN pip3 install -U pip
RUN mkdir /app/
WORKDIR /app/
RUN git clone -b v0.0.4a https://github.com/Itz-fork/Nexa-Userbot.git /app
RUN pip3 install -U -r requirements.txt
CMD bash startup.sh
