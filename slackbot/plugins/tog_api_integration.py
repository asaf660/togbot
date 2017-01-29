from slackbot.bot import respond_to
from TogglPy import Toggl
from utils import fetch_conf, get_projectId_by_name, get_projectName_by_id


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
    toggl_obj = toggl_user_object(message)
    if not toggl_obj:
        message.reply('Cannot use toggl with your name. Probably no Token set')
        return
    currentTime = toggl_obj.currentRunningTimeEntry()
    
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
    toggl_obj = toggl_user_object(message)
    if not toggl_obj:
        message.reply('Cannot use toggl with your name. Probably no Token set')
        return
    currentTime = toggl_obj.currentRunningTimeEntry()
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
    if not toggl_obj:
        message.reply('Cannot use toggl with your name. Probably no Token set')
        return
    currentTime = toggl_obj.currentRunningTimeEntry()

    if currentTime['data']:
        toggl_user_object(message).stopTimeEntry(currentTime['data']['id'])
        message.reply('Stopped.')
    else:
        message.reply('There is no time running')


@respond_to('set (.*) hours working on (.*)')
def entry(message, hours, parameters):
    if not toggl_obj:
        message.reply('Cannot use toggl with your name. Probably no Token set')
        return

    if len(parameters.split()) == 3:
        date = parameters.split()[2]
        startHour = None
    elif len(parameters.split()) == 5:
        date = parameters.split()[2]
        startHour = int(parameters.split()[4])
    else:
        date = None
        startHour = None

    project = parameters if len(parameters.split()) == 1 else parameters.split()[0]
    print 'parameters: ' + str(parameters) + ' len: ' + str(len(parameters.split()))
    print 'date: ' + date

    pid = get_projectId_by_name(project)
    if not pid:
        message.reply('No such project *{}*'.format(project))
        return

    day = int(date.split('.')[0]) if date else None
    month = int(date.split('.')[1]) if date else None
    year = int(date.split('.')[2]) if date else None

    try:
        response = toggl_obj.createTimeEntry(hourduration=int(hours), projectid=pid, year=year,
                                                                month=month, day=day, hour=startHour)
        print response
        ret_date = response['data']['start'].split('.')[0].split('T')[0]
        ret_time = response['data']['start'].split('.')[0].split('T')[1]
        ret_time_list = ret_time.split(':')
        ret_time_list[0] = str(int(ret_time_list[0]) + 2)
        ret_time = ':'.join(ret_time_list)
        message.reply('*Entry was set, {} hours working on {}* (`{}`)'.format(str(int(response['data']['duration']/3600)), 
                                                                            get_projectName_by_id(response['data']['pid']), 
                                                                            '{}, {}'.format(ret_date, ret_time)))
    except Exception as e:
        print e
        message.reply('Bad parameters (hours: {}, project: {}, pid {})'.format(hours, project, pid))
    

