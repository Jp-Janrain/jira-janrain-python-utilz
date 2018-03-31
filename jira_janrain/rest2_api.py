from __future__ import print_function

from jira import JIRA

from .utils import get_config, jira_date

ENV_VARS = {
    'JIRA_USER_NAME': '',
    'JIRA_USER_SECRET': '',
    'JIRA_DOMAIN': 'https://janrain.atlassian.net'
}


class Rest2():

    def __init__(self):
        config = get_config(ENV_VARS)
        self.creds = (config['JIRA_USER_NAME'], config['JIRA_USER_SECRET'])
        self.domain = config['JIRA_DOMAIN']
        self.url = '{}/rest/api/2'.format(self.domain)
        self.api = JIRA(server=self.domain, basic_auth=(self.creds))

    def search_all(self, jql, fields=['key'], max_results=100, expand=[]):
        issues = []
        start_at = 0
        total_results = max_results
        while total_results == max_results:
            results = self.api.search_issues(jql, fields=fields, startAt=start_at,
                                             maxResults=max_results, expand=expand)
            total_results = len(results)
            start_at += max_results
            issues.extend(results)
        return issues

    def get_worklogs(self, jql=None, start_date=None, end_date=None, authors=None):
        jql = 'issuetype in (standardIssueTypes(), subTaskIssueTypes())' \
            if not jql else jql
        worklogs = []
        if start_date:
            jql += ' AND worklogDate >= {}'.format(start_date)
        if end_date:
            jql += ' AND worklogDate <= {}'.format(end_date)
        if authors:
            jql += ' AND worklogAuthor in ({})'.format(authors)
        issues = self.search_all(jql, fields='summary, worklog')
        for issue in issues:
            if issue.fields.worklog.total > 20:
                issue_worklogs = self.api.worklogs(issue.key)
            else:
                issue_worklogs = issue.fields.worklog.worklogs
            for worklog in list(issue_worklogs):
                worklog.issue = issue
                if authors and worklog.author.key not in authors.split(', '):
                    issue_worklogs.remove(worklog)
                    continue
                if start_date and jira_date(worklog.started.split('T')[0]) < jira_date(start_date):
                    issue_worklogs.remove(worklog)
                    continue
                if end_date and jira_date(worklog.started.split('T')[0]) > jira_date(end_date):
                    issue_worklogs.remove(worklog)
                    continue
            worklogs.extend(issue_worklogs)
        return worklogs
