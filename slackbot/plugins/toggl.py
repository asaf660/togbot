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

@respond_to('^workspace$')
def toggl_report(message):
    response = toggl.request("https://www.toggl.com/api/v8/workspaces")
    print response
    for ws in response:
        message.reply('id: {} - {}'.format(ws['subscription']['workspace_id'], ws['name']))


@respond_to('^report ws$')
def toggl_report(message):
    response = toggl.request("https://toggl.com/reports/api/v2/weekly?workspace_id=0&user_agent=api_test")
    print response
    message.reply(str(response))


@respond_to('^users')
def toggl_report(message):
    response = toggl.request("https://www.toggl.com/api/v8/workspaces/0/users")
    # response = toggl.request("https://www.toggl.com/api/v8/clients")
    print response
    message.reply(str(response))


@respond_to('^dashboard')
def toggl_report(message):
    response = toggl.request("https://www.toggl.com/api/v8/dashboard/0")
    print response
    message.reply(response)

