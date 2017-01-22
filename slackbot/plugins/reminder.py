from slackbot.bot import respond_to

@respond_to('^go$')
def toggl_report(message):
    message.send(u"<!channel> Please make sure your Toggl reports a filled, I'll be reviewing them in one hour")