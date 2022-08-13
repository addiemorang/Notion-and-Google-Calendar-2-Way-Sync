import logging
import pickle
from datetime import datetime

from constants import CLIENT_SECRET_FILE_PATH, GOOGLE_CALENDAR_API_URL
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

from settings.config import CREDS_PATH, PROJECT_PATH


class GoogleService:

    def __init__(self):
        self.credentials = pickle.load(open(CREDS_PATH, "rb"))
        self.api = self.get_api_resource()

    def get_api_resource(self):
        try:
            return build('calendar', 'v3', credentials=self.credentials)
        except HttpError as e:
            logging.info(f'Error: {e}. Updating credentials')
            self.credentials = self.update_credentials()

            return build('calendar', 'v3', credentials=self.credentials)

    def get_calendar_event_data(self, calendar_id):
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + '-04:00'

        return self.api.events().list(
            calendarId=calendar_id,
            maxResults=2000,
            timeMin=now
        ).execute()

    def update_credentials(self):
        oauth_flow = InstalledAppFlow.from_client_secrets_file(
            f'{PROJECT_PATH}{CLIENT_SECRET_FILE_PATH}',
            scopes=[GOOGLE_CALENDAR_API_URL],
        )
        oauth_credentials = oauth_flow.run_console()

        # Not sure why we're doing this
        pickle.dump(oauth_credentials, open(CREDS_PATH, 'wb'))
        credentials = pickle.load(open(CREDS_PATH, 'rb'))

        return credentials