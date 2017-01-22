import os
from slackbot.bot import respond_to
from slackbot.bot import listen_to
from TogglPy import Toggl

toggl = Toggl()

toggl.setAPIKey(os.environ['TOGGL_API_KEY']) 

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

