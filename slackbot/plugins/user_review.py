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
        reportObject = toggl.getWeeklyReport({'workspace_id':'460285', 'user_ids':value})
        name = '<@{}>'.format(key.split()[0] if len(key.split()) > 1 else key)
        weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu']    # True only if executed on Thursday

        if not reportObject['data']:
            message.send('{}: you need to fill your entire week'.format(name))
        else:
            days = [day for day in reportObject['week_totals'][-6:-1]]
            for i, day in enumerate(days):
                days[i] = 0 if day is None else day/3600000
                    
            if 0 in days:
                weekly = ', '.join(['*{}* {}'.format(weekDays[i], day) for i, day in enumerate(days)])
                message.send('{}, Your week report: {}, Please complete it'.format(name, weekly))
                

            # response += '*{}* has {} hours over the past week \n'.format(key, [str(hours/3600000) for hours in reportObject['week_totals'] if hours is not None][-1])

        time.sleep(1)

    # message.reply(response)


@respond_to('^my time')
def print_users(message):
    pass

    



