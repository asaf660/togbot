# Create new toggl object (if previously not created - e.g toggl_omer)
# setAPIKey - if not in conf set im PM
# startTimeEntry
# currentRunningTimeEntry
# stopTimeEntry

# createTimeEntry
# randomizeTimeEntry

from slackbot.bot import respond_to

@respond_to('$set (.*) hours .* working on (.*)')
def entry(message, hours, project):
    print 'Hours: {}, Project: {}'.format(hours, project)
