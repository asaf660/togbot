import yaml
import os
import pickle

# Required only if deployed on a remote CI server e.g heroku 
# and conf.yml is not present:
EMPLOYEES = ['evgeny', 'leon', 'daniela', 'omer']

def fetch_conf():
    dataMap = {}
    try:
        with open('conf.yml') as conf:
            dataMap = yaml.safe_load(conf)
    except:
        dataMap['TOGGL_API_TOKEN'] = os.environ['TOGGL_API_TOKEN']
        dataMap['SLACK_API_TOKEN'] = os.environ['SLACK_API_TOKEN']
        
        for emp in EMPLOYEES:
            dataMap['USERS_TOKENS'][emp] = os.environ['TOGGL_API_TOKEN_{}'.format(emp.upper())]

    return dataMap


def get_projectId_by_name(projectName):
    projects = pickle.load(open( 'projectsMap.json', 'rb'))
    for key, value in projects.iteritems():
        if key.lower() in projectName.lower() or projectName.lower() in key.lower():
            return value
    
    return



if __name__ == '__main__':
    
    main()
    