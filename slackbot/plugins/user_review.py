from TogglPy import Toggl
from slackbot.bot import respond_to
import time
import yaml


def fetch_conf():
    with open('conf.yml') as conf:
        dataMap = yaml.safe_load(conf)
    return dataMap

toggl = Toggl()
toggl.setAPIKey(fetch_conf().get('TOGGL_API_TOKEN')) 


def users_dict():
    return {emp['fullname']: emp['id'] for emp in toggl.getWorkspaceUsers('460285')}


@respond_to('^users$')
def get_users(message):
    # reply = []
    # for emp in toggl.getWorkspaceUsers('460285'):
    #      '{}: {}'.format(emp['id'], emp['fullname'])
    message.reply('\n'.join(['{}: {}'.format(emp['id'], emp['fullname']) for emp in toggl.getWorkspaceUsers('460285')]))


@respond_to('^users report')
def user_report(message):
    response = ''
    for key, value in users_dict().iteritems():
        print '{}; {}'.format(key, value)
        reportObject = toggl.getWeeklyReport({'workspace_id':'460285', 'user_ids':value})
        if not reportObject['data']:
            response += '*{}* is missing time entries this week\n'.format(key)
        else:
            response += '*{}* has {} hours over the past week \n'.format(key, [str(hours/3600000) for hours in reportObject['week_totals'] if hours is not None][-1])
            #', '.join([str(hours/3600000) for hours in reportObject['week_totals'] if hours is not None])
        time.sleep(1)

    message.reply(response)

    



