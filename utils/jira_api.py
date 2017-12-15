from jira import JIRA
from jira.exceptions import JIRAError
from utils.setting import project_name, options, usr, pas
import pandas as pd


def get_jira_tasks(start_date, end_date):
    """
    Get Jira Task API
    :param start_date: YYYY-MM-DD
    :param end_date: YYYY-MM-DD
    :return: DataFrame
    """

    start_date=start_date.replace("-",'/')
    end_date=end_date.replace("-",'/')
    try:
        jira = JIRA(options=options, basic_auth=(usr, pas))
    except JIRAError as e:
        if e.status_code == 401:
            print ("Login to JIRA failed.")
    jq = """project = {} 
    and duedate >= "{}" 
    and duedate <= "{}" 
    order by created DESC""".format(project_name, start_date,end_date )
    issues = jira.search_issues(jq)
    columns = ['year','month','day', 'name','timeoriginalestimate','timespent']
    data = pd.DataFrame([], columns=columns)
    for issue in issues:
        name = "NoAssign"
        if issue.fields.assignee:
            name = issue.fields.assignee.displayName
        (year, month, day) = issue.fields.duedate.split("-")
        timeoriginalestimate = issue.fields.timeoriginalestimate if issue.fields.timeoriginalestimate is not None else 0
        timespent = issue.fields.timespent if issue.fields.timespent is not None else 0
        tmp_df = pd.DataFrame([[year, month, day, name, timeoriginalestimate/3600, timespent/3600]], columns=columns)
        data = data.append(tmp_df)

    data.reset_index(drop=True, inplace=True)
    return data
