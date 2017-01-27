import yaml
import os
from slackbot.plugins.utils import fetch_conf


API_TOKEN = fetch_conf().get('SLACK_API_TOKEN')
DEFAULT_REPLY = "YO!"
PLUGINS = [
    'slackbot.plugins',
]