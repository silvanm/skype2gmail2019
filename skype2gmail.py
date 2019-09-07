from datetime import datetime, timedelta
import pytz as pytz

import json
import os

from clients.gmail_client import GmailClient
from lib.importlib import process_conversation

gmail_client = GmailClient()

with open("messages.json", 'r') as f:
    messages = json.load(f)

# read status (last update) from disk
status_file_path = os.path.join("var", "status.json")
if os.path.exists(status_file_path):
    status = json.load(open(status_file_path))
else:
    status = {
        'last_update_ts': int((datetime.now() - timedelta(weeks=1)).strftime("%s"))
    }
print(
    "Processing all messages since %s" % datetime.fromtimestamp(status['last_update_ts'], tz=pytz.UTC).strftime(
        "%a, %d.%m.%y, %H:%M %Z"))

for conversation in messages['conversations']:
    process_conversation(conversation, gmail_client, since=datetime.fromtimestamp(status['last_update_ts']))

# write new status to disk
status['last_update_ts'] = int(datetime.now().strftime("%s"))
json.dump(status, open(status_file_path, 'w'))
