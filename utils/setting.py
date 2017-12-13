# JIRA API Setting
import os

project_name = os.getenv('JIRA_PJ', 'project_name')
options = {
    'server': os.getenv('JIRA_URL', 'https://projectName.atlassian.net')
}
usr = os.getenv('JIRA_USER', 'user')
pas = os.getenv('JIRA_PASS', 'password')