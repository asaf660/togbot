#!/usr/bin/env python

import sys
import os
import logging
import logging.config
from slackbot import settings
from slackbot.bot import Bot
import yaml
import flask
app = flask.Flask(__name__)

@app.route("/")
def index():
    #do whatevr here...
    return "Hello Heruko"
    
def main():
    kw = {
        'format': '[%(asctime)s] %(message)s',
        'datefmt': '%m/%d/%Y %H:%M:%S',
        'level': logging.DEBUG if settings.DEBUG else logging.INFO,
        'stream': sys.stdout,
    }
    logging.basicConfig(**kw)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)
    bot = Bot()
    bot.run()


if __name__ == '__main__':

    main()
