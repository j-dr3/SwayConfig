#!/home/jd/.config/waybar/scripts/bin/python3
from slack_sdk import WebClient
import configparser
import os
import sys
from datetime import datetime, timedelta
import json
import random

config = configparser.ConfigParser()
config.read(os.path.expanduser("~") + "/.config/cyon/config")
token = config['slack']['token']

now = datetime.now()

stati = {
    "brb": [":brb:", "Gleich wieder da", now.replace(hour=23, minute=59, second=59, microsecond=999999)],
    "datacenter": [":iwb:", "im IWB Datacenter", now.replace(hour=23, minute=59, second=59, microsecond=999999)],
    "focus": [":brain:", "Focus", now + timedelta(hours=1)],
    "focus": [":brain:", "Focus", now + timedelta(hours=1)],
    "home": [":house_with_garden:", "@home", now.replace(hour=23, minute=59, second=59, microsecond=999999)],
    "laufen": [":man-walking:", "Kurz ne runde laufen, gleich wieder da :blush:", now + timedelta(minutes=30)],
    "maintenance": [":construction: ", "Wartungsarbeiten", now.replace(hour=8, minute=0, second=0, microsecond=0) + timedelta(hours=24)],
    "mittag": [":chompy:", "Am Essen", now + timedelta(minutes=60)],
    "none": ["", "", 0],
    "office": [":office:", "Im Büro", now.replace(hour=23, minute=59, second=59, microsecond=999999)],
    "offline": [":mobile_phone_off:", "Off Work", now.replace(hour=8, minute=0, second=0, microsecond=0) + timedelta(hours=24)],
    "train": [":train:", "Im Zug", now + timedelta(minutes=45)],
    "zivilschutz": [":zivilschutz:", "Zivilschutz", 0],
    "off": [":zzz:", "Off Work", now.replace(hour=8, minute=0, second=0, microsecond=0) + timedelta(hours=24)],
    "schule": [":school:", "In der schule", now.replace(hour=8, minute=0, second=0, microsecond=0) + timedelta(hours=24)]
        }        

onoff_msgs = {
    "mörgeli": [":wave:", "Guten Morgen :smile:", ":v:"],
    "bye": [":wave:", "Schönen Abend :wave:", "Bis morgen :v:"],
    "mittag": [":chompy:"],
    "weekend": ["Schönes Wochenende :wave:"],
}

client = WebClient(token=token)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.stderr.write(
            "Wrong number of params provided (%s instead of 1)" % str(len(sys.argv) - 1))
        exit(1)
    elif sys.argv[1] == 'status':

        profile = client.users_profile_get()['profile']

        data = {
            "text": " %s" % (profile['status_text'] if profile['status_text'] else "None"),
            "alt": "Slack Status",
        }

        sys.stdout.write(json.dumps(data) + '\n')
        sys.stdout.flush()

    elif sys.argv[1] == 'stati':
        for status in stati:
            print("[status] - " + status)

        for msg in onoff_msgs:
            print("[onoff] - " + msg)

    else:

        action = sys.argv[1].split(" - ")[1]

        if action in stati:

            if stati[action][2] != 0:
                client.users_profile_set(profile={
                    "status_text": stati[action][1],
                    "status_emoji": stati[action][0],
                    "status_expiration": int(stati[action][2].timestamp())
                })
            else:
                client.users_profile_set(profile={
                    "status_text": stati[action][1],
                    "status_emoji": stati[action][0]
                })

            if action == "focus":
                client.dnd_setSnooze(num_minutes=60)
            elif action == "none":
                client.dnd_endDnd()

        elif action in onoff_msgs:
            msg = random.choice(onoff_msgs[action])
            client.chat_postMessage(channel="C02JZ6E18N9", text=msg)

        else:
            sys.stderr.write(
                "The status '%s' could not be found." % sys.argv[1])
            exit(1)
