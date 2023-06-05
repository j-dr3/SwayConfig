#!/usr/bin/env python3
import os
import requests
import json
import sys
import configparser
import time

config = configparser.ConfigParser()
config.read(os.path.expanduser("~") + "/.config/cyon/config")

def get_timer():

  return requests.get("https://%s.hakuna.ch/api/v1/timer" % config['hakuna']['tenant'], headers={'X-Auth-Token': config['hakuna']['token']}).json()

def start_timer():

  requests.post("https://%s.hakuna.ch/api/v1/timer" % config['hakuna']['tenant'], headers={'X-Auth-Token': config['hakuna']['token']}, data={'task_id': 2})

def stop_timer():

  requests.put("https://%s.hakuna.ch/api/v1/timer" % config['hakuna']['tenant'], headers={'X-Auth-Token': config['hakuna']['token']})

def toggle_timer():

  timer = get_timer()

  if (timer['duration_in_seconds']) == 0:
    start_timer()
  else:
    stop_timer()

if __name__ == '__main__':
  
  if len(sys.argv) != 2:
    sys.stderr.write("Wrong number of params provided (%s instead of 1)" % str(len(sys.argv) - 1))
    exit(1)

  elif sys.argv[1] == 'status':

    time.sleep(1)

    res = get_timer()
    tooltip = res['user']['name'] + " - " + res['user']['email'] + " - " + res['user']['groups'][0]
    status = 'running' if res['duration_in_seconds'] != 0 else ''

    icon = '' if status == 'running' else ''

    data = {
      "text": icon + ' ' + res['duration'],
      "alt": "alt",
      "tooltip": tooltip,
      "class": status
    }

    sys.stdout.write(json.dumps(data) + '\n')
    sys.stdout.flush()

  elif sys.argv[1] == 'toggle':
  
    toggle_timer()
    
  else:
  
    sys.stderr.write("Action '%s' is invalid..." % sys.argv[1])
    exit(1)

