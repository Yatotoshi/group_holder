import json
import urllib.request


# def update_group_list():
    # get_parameters = "/bot198334737:AAH3Z-0Gu1TqnVj6H8Zs3f4OS8u71JeX5Jc"
    # response = urllib.request.urlopen("https://api.telegram.org" + get_parameters + "getUpdates")
    # response


# json.dump(victims, open('victims.txt', 'w'))
absorbers = [
    {
        "id": "-154379887",
        "name": "Test Group"
    },
    {
        "id": "154427173",
        "name": "Test Group 2"
    }
]

json.dump(absorbers, open('absorbers.txt', 'w'))
# victims = json.load(open('victims.txt', 'r'))
