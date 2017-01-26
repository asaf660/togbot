import yaml
import os

def fetch_conf():
    dataMap = {}
    try:
        with open('conf.yml') as conf:
            dataMap = yaml.safe_load(conf)
    except:
        dataMap['TOGGL_API_TOKEN'] = os.environ['TOGGL_API_TOKEN']
        dataMap['SLACK_API_TOKEN'] = os.environ['SLACK_API_TOKEN']

    return dataMap

API_TOKEN = fetch_conf().get('SLACK_API_TOKEN')
DEFAULT_REPLY = "YO!"
PLUGINS = [
    'slackbot.plugins',
]