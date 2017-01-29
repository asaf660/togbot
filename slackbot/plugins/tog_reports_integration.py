from TogglPy import Toggl
from slackbot.bot import respond_to
import time
import yaml
from apscheduler.scheduler import Scheduler  # pip install apscheduler==2.1.2
from datetime import datetime
from collections import deque
import os
from utils import fetch_conf
import pickle

REMINDER_ACTIVATED = {}


toggl = Toggl()
toggl.setAPIKey(fetch_conf().get('TOGGL_API_TOKEN')) 
sched = Scheduler()
sched.start()


def humanize_time(day):
    hours = day/3600000
    minutes = int(((float(day)/3600000) % 1) * 60)

    return hours, minutes


def shift(arr, num):
    items = deque(arr)
    items.rotate(num)
    return list(items)


def get_fixed_days():
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    today = datetime.today().weekday()
    return shift(days, -1) if today == 6 else shift(days, 5-today)
        
    
def users_dict():
    return {emp['fullname']: emp['id'] for emp in toggl.getWorkspaceUsers('460285')}


@respond_to('^create projects map$')
def create_projects_map(message):
    toggl.createProjectsMap()


@respond_to('help')
def help(message):
    options = [
        'Instructions:',
        'In a channel call me like any other user by tagging: *@togbot <message>*',
        'In private you can just send your request, for now I do these:',
        '1. *get users report* will notify users with empty / part empty reports',
        '2. *my report* will get your own last 7 days report (excluding weekend)',
        '3. *activate* is used to make me report on Thursday at 17:00 (do it only once)',
        '4. *start time <project>* can start the timer (if the given name matches a Toggl project)',
        '5. *current time* returns the start time',
        '6. *stop time* stops current running time',
        '7. *set 3 hours working on mdx* sets an entry for today starting at 9:00',
        '8. *set 8 hours working on 90min on 29.1.2017* like (7) with explicit date',
        '9. *set 5 hours working on tapingo on 15.1.2017 from 16* like (8) with starting hour',
        '\n',
        'People I can currently help with differnt Toggl tasks (5-9) are:',
        ', '.join([name for name in fetch_conf()['USERS_TOKENS'].keys()])
    ]
    message.reply('\n'.join(options))


@respond_to('^users$')
def get_users(message):
    message.reply('\n'.join(['{}: {}'.format(emp['id'], emp['fullname']) for emp in toggl.getWorkspaceUsers('460285')]))


@respond_to('get users report')
def users_report(message):
    empty_week_users = []
    for key, value in users_dict().iteritems():
        reportObject = toggl.getWeeklyReport({'workspace_id':'460285', 'user_ids':value})
        name = '<@{}>'.format(key.split()[0] if len(key.split()) > 1 else key)

        if not reportObject['data']:
            # message.send('{}: your week is empty'.format(name))
            empty_week_users.append(name)
        else:
            weekDays = get_fixed_days()
            days = [day for day in reportObject['week_totals'][:7]]
            for i, day in enumerate(days):
                if day is None:
                    days[i] = 0
                else:
                    hours, minutes = humanize_time(day)
                    days[i] = '{}:{}'.format(hours, minutes) if minutes else hours

            summary = {weekDays[i]: day for i, day in enumerate(days) if weekDays[i] not in ['Fri', 'Sat']}
            if 0 in summary.values():
                weekly = ', '.join(['*{}* {}'.format(weekDays[i], day) for i, day in enumerate(days) if weekDays[i] not in ['Fri', 'Sat']])
                message.send('{}! Not good enough: {}'.format(name, weekly))

        
        time.sleep(1)  # Toggl API limitations

    if len(empty_week_users) > 0:
            message.send('{}, your week is empty, why?\n\n\n{}'.format(' ,'.join(empty_week_users), 'FINISH IT! https://toggl.com/app/timer'))                



@respond_to('^activate$')
def activation(message):
    global REMINDER_ACTIVATED
    if not REMINDER_ACTIVATED.get(message.body['channel']):
        job = sched.add_cron_job(users_report, day_of_week=3, hour=17, minute=0)
        REMINDER_ACTIVATED[message.body['channel']] = True
        message.send('Activated, I will report every Thursday')
    else:
        message.send('Already activated.')
    

@respond_to('my report')
def self_report(message):
    name = message.get_user_name().lower()
    for key, value in users_dict().iteritems():
        if key.split()[0].lower() == name:
            reportObject = toggl.getWeeklyReport({'workspace_id':'460285', 'user_ids':value})
            break      
    
    weekDays = get_fixed_days()
    days = [day for day in reportObject['week_totals'][:7]]
    for i, day in enumerate(days):
        if day is None:
            days[i] = 0
        else:
            hours, minutes = humanize_time(day)
            days[i] = '{}:{}'.format(hours, minutes) if minutes else hours
                
    weekline = ', '.join(['*{}* {}'.format(weekDays[i], day) for i, day in enumerate(days) if weekDays[i] not in ['Fri', 'Sat']])
    message.reply('{}\n{}'.format('You week entires (today is the last entry to the right):', weekline))

@respond_to('message')
def message(message):
    print 'running: {}'.format(toggl.currentRunningTimeEntry())



# TODO: WIP ------>
# @respond_to('$set (.*) hours .* working on (.*)')
# def set_entry(message, hours, project):
#     if 'today' in message.body:
#         toggl.createTimeEntry()


if __name__ == '__main__':
    
    main()
