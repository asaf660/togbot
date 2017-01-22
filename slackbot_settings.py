import yaml

def fetch_conf():
    with open('conf.yml') as conf:
        dataMap = yaml.safe_load(conf)
    return dataMap

API_TOKEN = fetch_conf().get('SLACK_API_TOKEN')
DEFAULT_REPLY = "Sorry but I didn't understand you"
PLUGINS = [
    'slackbot.plugins',
]