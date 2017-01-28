import yaml
import os
from slackbot.bot import respond_to


def fetch_conf():
    dataMap = {}
    try:
        with open('conf.yml') as conf:
            dataMap = yaml.safe_load(conf)
    except:
        dataMap['TOGGL_API_TOKEN'] = os.environ['TOGGL_API_TOKEN']
        dataMap['SLACK_API_TOKEN'] = os.environ['SLACK_API_TOKEN']

    return dataMap


@respond_to('^cpm$')
def create_projects_map():
    PROJECTS_MAP = toggl.createProjectsMap()
    print PROJECTS_MAP


if __name__ == '__main__':
    
    main()
    