import yaml
from slackbot.bot import respond_to
from slackbot.bot import listen_to
from TogglPy import Toggl


def fetch_conf():
    with open('conf.yml') as conf:
        dataMap = yaml.safe_load(conf)
    return dataMap

toggl = Toggl()
toggl.setAPIKey(fetch_conf().get('TOGGL_API_TOKEN')) 


@respond_to('^dashboard')
def toggl_report(message):
    response = toggl.request("https://www.toggl.com/api/v8/dashboard/0")
    print response
    message.reply(response)

