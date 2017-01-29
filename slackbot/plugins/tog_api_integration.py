# Create new toggl object (if previously not created - e.g toggl_omer)
# setAPIKey - if not in conf set im PM
# startTimeEntry
# currentRunningTimeEntry
# stopTimeEntry

# createTimeEntry
# randomizeTimeEntry

from slackbot.bot import respond_to
from TogglPy import Toggl
from utils import fetch_conf, get_projectId_by_name


def toggl_user_object(message):
    conf = fetch_conf().get('USERS_TOKENS')
    username = message.get_user_name().lower()
    if not conf or not conf[username]: 
        return
    
    toggl_user_object = Toggl()
    toggl_user_object.setAPIKey(conf[username]) 
    return toggl_user_object


@respond_to('^current time')
def currentRunningTime(message):
    currentTime = toggl_user_object(message).currentRunningTimeEntry()
    if not currentTime['data']:
        message.reply('No current running time')
    else:
        sinceTime = currentTime['data']['start'].split('T')[1].split('+')[0]
        hours = sinceTime.split(':')[0]
        minutes = sinceTime.split(':')[1]
        if int(hours) < 22: 
            hours = str(int(hours) + 2)
        elif int(hours) == 22:
            hours = 0
        elif int(hours) == 23:
            hours = 1

        message.reply('Time running since *{}:{}*'.format(hours, minutes))


@respond_to('^start time (.*)')
def startTime(message, project=None):
    currentTime = toggl_user_object(message).currentRunningTimeEntry()
    if not currentTime['data']:
        # Find pid by given project name
        pid = get_projectId_by_name(project)
        if not pid:
            message.reply('No such project "{}"'.format(project))
        else:
            toggl_user_object(message).startTimeEntry('', pid)
            message.reply('Started, time is running')
    else:
        message.reply('Time is already running')


@respond_to('^stop time$')
def startTime(message,):
    currentTime = toggl_user_object(message).currentRunningTimeEntry()

    if currentTime['data']:
        toggl_user_object(message).stopTimeEntry(currentTime['data']['id'])
        message.reply('Stopped.')
    else:
        message.reply('There is no time running')


@respond_to('set (.*) hours working on (.*)')
def entry(message, hours, project):
    pid = get_projectId_by_name(project)
    if not pid:
        message.reply('No such project *{}*'.format(project))
        return
    try:
        toggl_user_object(message).createTimeEntry(hourduration=int(hours), projectid=pid)
    except Exception as e:
        print e
        message.reply('Bad parameters (hours: {}, project: {}, pid {})'.format(hours, project, pid))
    


