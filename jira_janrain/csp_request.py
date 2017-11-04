from __future__ import print_function

from .rest2_api import Rest2


class CSPRequest():

    def __init__(self, issue_key):
        self.key = issue_key
        self.url = 'https://janrain.atlassian.net/browse/{}'.format(issue_key)
        self.issue = Rest2().api.issue(issue_key)

        fields = self.issue.fields
        self.summary = fields.summary
        self.assignee = fields.assignee
        self.status = fields.status
        self.worklog = fields.worklog
        self.status = fields.status
        self.created = fields.created
        self.priority = fields.priority
        self.reporter = fields.reporter
        self.components = fields.components
        self.issuetype = fields.issuetype
        self.resolutiondate = fields.resolutiondate
        self.customer = fields.customfield_10500
        self.technical_account_manager = fields.customfield_16801
        self.project_manager = fields.customfield_13202
        self.customer_priority = fields.customfield_17202
        self.customer_impact = fields.customfield_20100
        self.organizations = fields.customfield_18700

    def raw(self, expand=None):
        """Get the full raw object"""
        return Rest2().api.issue(self.key, expand=expand).raw

    def worklogs(self, start_date=None, end_date=None, authors=None):
        jql = '(issue = {})'.format(self.key)
        return Rest2().get_worklogs(jql, start_date=start_date, end_date=end_date, authors=authors)