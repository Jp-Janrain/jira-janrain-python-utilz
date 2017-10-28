import os

from datetime import datetime as dt

def get_config(ENV_VARS):
    config = {}
    for key, default_value in ENV_VARS.items():
        value = os.getenv(key, default_value)
        # empty string means use default value
        if value is '':
            value = default_value
        if isinstance(ENV_VARS[key], bool) and not isinstance(value, bool):
            if value.upper() != 'FALSE':
                value = True
            else:
                value = False
        elif isinstance(ENV_VARS[key], int) and not isinstance(value, int):
            try:
                value = int(value)
            except ValueError:
                value = 0
        config[key] = value
    return config


def valid_date(date):
    try:
        dt.strptime(date, "%Y-%m-%d")
        return date
    except ValueError:
        raise "'{}' is not a valid date format.\n Please use: YYYY-MM-DD".format(
            date)

def jira_date(date_string):
    return dt.strptime(date_string, '%Y-%m-%d')