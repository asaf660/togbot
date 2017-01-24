from TogglPy import Toggl
from slackbot.bot import respond_to
import time
import yaml
from apscheduler.scheduler import Scheduler  # pip install apscheduler==2.1.2
from datetime import datetime
from collections import deque


def fetch_conf():
    with open('conf.yml') as conf:
        dataMap = yaml.safe_load(conf)
    return dataMap

toggl = Toggl()
toggl.setAPIKey(fetch_conf().get('TOGGL_API_TOKEN')) 
sched = Scheduler()
sched.start()


def shift(arr, num):
    items = deque(arr)
    items.rotate(num)
    return list(items)


def fix_days(days):
    today = datetime.today().weekday()
    return shift(days, -1) if today == 6 else shift(days, 5-today)
        
    
def users_dict():
    return {emp['fullname']: emp['id'] for emp in toggl.getWorkspaceUsers('460285')}


@respond_to('^users$')
def get_users(message):
    message.reply('\n'.join(['{}: {}'.format(emp['id'], emp['fullname']) for emp in toggl.getWorkspaceUsers('460285')]))


@respond_to('send users report')
def users_report(message):
    for key, value in users_dict().iteritems():
        reportObject = toggl.getWeeklyReport({'workspace_id':'460285', 'user_ids':value})
        name = '<@{}>'.format(key.split()[0] if len(key.split()) > 1 else key)
        weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']    # True only if executed on Thursday

        if not reportObject['data']:
            message.send('{}: your week is empty'.format(name))
        else:
            days = [day for day in reportObject['week_totals'][:7]]
            weekDays = fix_days(weekDays)
            for i, day in enumerate(days):
                days[i] = 0 if day is None else day/3600000

            summary = {weekDays[i]: day for i, day in enumerate(days) if weekDays[i] not in ['Fri', 'Sat']}
            if 0 in summary.values():
                weekly = ', '.join(['*{}* {}'.format(weekDays[i], day) for i, day in enumerate(days) if weekDays[i] not in ['Fri', 'Sat']])
                message.send('{}, Your week report is not complete: {}'.format(name, weekly))

        time.sleep(1)  # Toggl API limitations


@respond_to('^activate$')
def activation(message):
    # job = sched.add_cron_job(users_report, dat_of_week=3, hour=17, minute=0)
    job = sched.add_cron_job(users_report, minute=29, args=[message])
    message.send('Activated, I will report every Thursday')

    
if __name__ == '__main__':
    
    main()
