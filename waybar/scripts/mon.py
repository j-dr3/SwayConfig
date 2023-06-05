#!/usr/bin/env python3
import requests
import json
import sys


def get_status():

    res = requests.get(
        "https://mon-icinga01.cyon.io/icingaweb2/ampel_status.php",
        verify=False
    )

    if res.status_code == 200:
        status = int(res.text)

    data = {
        "text": "",
        "class": "",
        "tooltip": "",
    }

    if status == 0:
        data['class'] = "ok"
        data['tooltip'] = "Alles paletti :)"
    elif status == 1:
        data['class'] = "warn"
        data['tooltip'] = "Da scheint was im Busch zu sein..."
    elif status == 2:
        data['class'] = "error"
        data['tooltip'] = "Die Kacke ist am dampfen..."

    sys.stdout.write(json.dumps(data) + '\n')
    sys.stdout.flush()


if __name__ == '__main__':

    get_status()
