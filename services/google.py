import logging
import pickle

from constants import CLIENT_SECRET_FILE_NAME, GOOGLE_CALENDAR_API_URL
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow


class GoogleService:

    def __init__(self):
        self.credentials = self.get_credentials()
        self.service = build('calendar', 'v3', credentials=self.credentials)

    def get_calendar_resource(self, calendar_id):
        try:
            calendar = self.service.calendars().get(calendarId=calendar_id).execute()
            return calendar
        except HttpError as e:
            logging.info(e)

    def get_credentials(self):
        oauth_flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE_NAME, scopes=[GOOGLE_CALENDAR_API_URL])
        oauth_credentials = oauth_flow.run_console()

        # Not sure why we're doing this
        pickle.dump(oauth_credentials, open('token.pkl', 'wb'))
        credentials = pickle.load(open('token.pkl', 'rb'))

        return credentials