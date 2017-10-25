from __future__ import print_function

import requests

from .utils import get_config

ENV_VARS = {
    'JIRA_USER_NAME': '',
    'JIRA_USER_SECRET': '',
    'JIRA_DOMAIN': 'https://janrain.atlassian.net'
}


class Desk:

    def __init__(self, creds):
        self.url = 'https://janrain.atlassian.net/rest/servicedeskapi'
        config = get_config(ENV_VARS)
        self.creds = (config['JIRA_USER_NAME'], config['JIRA_USER_SECRET'])

    def get(self, path, parameters=None):
        """makes a GET call

        Keyword Arguments:
        path -- complete path from base url (ex: issues/CSP-1234)
        params -- keyword dictionary of query parameters
        """
        endpoint = '{}/{}'.format(self.url, path)
        return requests.get(endpoint,
                            auth=self.creds,
                            params=parameters)
