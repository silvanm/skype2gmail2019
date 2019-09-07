import base64
import os
from email.mime.text import MIMEText
from email.utils import formatdate

import httplib2
from apiclient import discovery
from googleapiclient import errors
from oauth2client import client, tools
from oauth2client.file import Storage
from datetime import date, datetime

from config import *

SCOPES = 'https://www.googleapis.com/auth/gmail.compose https://www.googleapis.com/auth/gmail.modify'
CLIENT_SECRET_FILE = 'etc/client_secret.json'
APPLICATION_NAME = 'Slack2Gmail'


class GmailClient:
    """
    Encapsulates all interaction with the Gmail API
    """

    def __init__(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('gmail', 'v1', http=http)

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        credential_path = os.path.join('etc',
                                       'gmail_credentials.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def users_to_string(self, users):
        return " ".join([f"{user['name']} <{user['email']}>" for user in users])

    def create_message(self, sender, to, subject, message_text, date: date):
        message = MIMEText(message_text, 'html', 'utf-8')
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        message['date'] = formatdate(datetime.combine(date, datetime.min.time()).timestamp())
        msg_dict = {
            'raw': base64.urlsafe_b64encode(bytes(message.as_string(), 'utf-8')).decode('ascii'),
            'labelIds': [GMAIL_LABEL],
        }

        try:
            message_obj = self.service.users().messages().insert(userId='me', body=msg_dict,
                                                                 internalDateSource='dateHeader').execute()
            return message_obj
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
            return None
