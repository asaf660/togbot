FROM python:2.7-alpine

RUN mkdir -p /togbot
WORKDIR /togbot

RUN apk add --update git \
    && git clone https://github.com/omerxx/togbot.git . \
    && pip install -r requirements.txt

COPY conf.yml .

CMD ["python", "run.py"]
