from __future__ import print_function

from .rest2_api import Rest2


class TamEpic(Rest2):

    def __init__(self, issue_key):
        _fields = '''summary, assignee, customfield_10500, customfield_16801,
        customfield_13202, customfield_13600, customfield_20602, customfield_13601,
        worklog'''

        self.key = issue_key
        self.issue = Rest2().api.issue(issue_key, fields=_fields)
        self.raw = self.issue.raw

        fields = self.issue.fields
        self.summary = fields.summary
        self.assignee = fields.assignee
        self.customer = fields.customfield_10500
        self.technical_account_manager = fields.customfield_16801
        self.project_manager = fields.customfield_13202
        self.start_date = fields.customfield_13600
        self.end_date = fields.customfield_13601
        self.contracted_hours = fields.customfield_20602
        self.worklog = fields.worklog

    def get_billable_worklogs(self, start_date=None, end_date=None, authors=None):
        jql = 'issuetype not in ("Un-billable - Janrain Troubleshooting", "Un-billable - Project Work")\
        AND (issue = {x} OR "Epic Link" = {x} OR parent = {x})'.format(x=self.key)
        return Rest2().get_worklogs(jql, start_date=start_date, end_date=end_date, authors=authors)

    def get_all_worklogs(self, start_date=None, end_date=None, authors=None):
        jql = '(issue = {x} OR "Epic Link" = {x} OR parent = {x})'.format(x=self.key)
        return Rest2().get_worklogs(jql, start_date=start_date, end_date=end_date, authors=authors)
