#!/usr/bin/env python

import sys
import os
import logging
import logging.config
from slackbot import settings
from slackbot.bot import Bot
import yaml


def fetch_conf():
    with open('conf.yml') as conf:
        dataMap = yaml.safe_load(conf)
    return dataMap


def set_env(dataMap):
    for key, value in dataMap.iteritems():
        print 'Setting {} = {}'.format(key, value)
        os.environ[key] = dataMap.get(key)


def main():
    set_env(fetch_conf())
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