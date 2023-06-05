#!/usr/bin/env python3
import requests
import json
import sys
import os
import configparser

config = configparser.ConfigParser()
config.read(os.path.expanduser("~") + "/.config/cyon/config")

token = config['jira']['token']
base_url = "%s/rest/api/2" % config['jira']['instance']

headers = {
    'Authorization': "Bearer %s" % token
}


def get_count_by_query(query):

    query_string = {"jql": "%s" % query}

    res = requests.get(base_url + "/search", data="",
                       headers=headers, params=query_string).json()
    return res['total']


if __name__ == '__main__':

    my_open = get_count_by_query(
        "assignee=currentUser() AND resolution = Unresolved")
    reported_open = get_count_by_query(
        "reporter = currentUser() AND resolution = Unresolved")
    inbox_unassigned = get_count_by_query(
        'project = CYON AND team = SYS AND status = "To Do" AND resolution = Unresolved AND assignee is EMPTY')

    data = {
        "text": " %s|%s|%s" % (my_open, reported_open, inbox_unassigned),
        "alt": "Jira Issues",
        "tooltip": "My Open: %s\nMy Reported and Open: %s\nInbox SYS: %s" % (my_open, reported_open, inbox_unassigned),
        "class": "status",
        "percentage": "0"
    }

    sys.stdout.write(json.dumps(data) + '\n')
    sys.stdout.flush()
