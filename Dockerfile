FROM python:3.8-buster


ADD . /code
WORKDIR /code

RUN pip install -r /code/requirements.txt

RUN apt-get update && apt-get install -y cron
COPY crontab /code/crontab
RUN crontab /code/crontab
RUN chmod +x /code/project/etl.py

ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

CMD /wait && python /code/project/etl.py;cron -L 2 -f
