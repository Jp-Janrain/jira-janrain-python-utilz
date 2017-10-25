from __future__ import print_function

from jira import JIRA

from .utils import get_config

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

    def get_worklogs(self, jql, start=None, end=None, authors=None):
        worklogs = []
        if start:
            jql += ' AND worklogDate >= {}'.format(start)
        if end:
            jql += ' AND worklogDate <= {}'.format(end)
        if authors:
            jql += ' AND worklogAuthor in ({})'.format(authors)
        issues = self.search_all(jql, fields='worklog')
        for issue in issues:
            if issue.fields.worklog.total > 20:
                issue_worklogs = self.api.worklogs(issue.key)
            else:
                issue_worklogs = issue.fields.worklog.worklogs
            print('{}: {}'.format(issue.key, len(issue_worklogs)))
            for worklog in issue_worklogs:
                if authors and worklog.author.key in authors.split(', '):
                    print(worklog.author.key)
    # TODO: filter worklog results to logs that match time/person filters
