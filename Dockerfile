FROM ubuntu:latest

RUN apt-get update && apt-get -y install python3.9 && apt-get -y install python3-pip && apt-get -y install cron

COPY ./requirements.txt /tmp/

COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab
RUN touch /var/log/cron.log

RUN pip3 install -r /tmp/requirements.txt

RUN useradd --create-home app

WORKDIR /home/app

RUN mkdir crawler
RUN mkdir server

COPY crawler crawler
COPY server server

RUN chmod +x crawler/run_crawler
RUN crawler/run_crawler

CMD cron && python3 /home/app/server/server.py
