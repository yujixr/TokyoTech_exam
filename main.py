import csv
import os
from datetime import date

from requests_oauthlib import OAuth1Session


def get_next_event(filename, today):
    next_event = None
    with open(filename, "r") as f:
        for row in csv.reader(f):
            name = row[0]
            year = int(row[1])
            month = int(row[2])
            day = int(row[3])

            scheduled_date = date(year, month, day)
            if scheduled_date > today:
                next_event = [name, str((scheduled_date - today).days)]
                break
    return next_event

EXAMS_FILE = os.getenv("EXAMS_FILE")
EVENTS_FILE = os.getenv("EVENTS_FILE")

today = date.today()
next_exam = get_next_event(EXAMS_FILE, today)
next_event = get_next_event(EVENTS_FILE, today)

status = ""
if next_exam is not None:
    status += next_exam[0] + "まであと" + next_exam[1] + "日です。\n"
if next_event is not None:
    status += next_event[0] + "まであと" + next_event[1] + "日です。\n"
print(status)

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

params = { "status": status }
res = twitter.post("https://api.twitter.com/1.1/statuses/update.json", params = params)
print(res.status_code, res.text)
