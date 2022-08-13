from datetime import datetime

from app.constants import GOOGLE_CALENDAR_STRPTME_FMT, GOOGLE_CALENDAR_STRPTME_FMT_DT


class Calendar:

    def __init__(self, name, calendar_id, service):
        self.name = name
        self.calendar_id = calendar_id
        self.service = service

        self.events = []

    def initialize_events(self):
        fetched_events = self._fetch_events()

        for event in fetched_events:
            event_start = event['start']
            event_end = event['end']
            if 'dateTime' in event_start.keys().update(event_end.keys()):
                start = self._to_python_datetime(event['start']['dateTime'])
                end = self._to_python_datetime(event['end']['dateTime'])
            else:
                start = self._to_python_date(event['start']['dateTime'])
                end = self._to_python_date(event['end']['dateTime'])

            event_kwargs = {
                'name': 'summary',
                'calendar': self,
                'start': start,
                'end': end,
                'id': event['id'],
                'description': event['description']
            }

            new_event = Event(**event_kwargs)
            self.events.append(new_event)

    def _fetch_events(self):
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + '-04:00'

        return self.service.events().list(
            calendarId=self.calendar_id,
            maxResults=2000,
            timeMin=now
        ).execute()

    def _to_python_datetime(self, google_calendar_datetime):
        return datetime.strptime(google_calendar_datetime[:-6], GOOGLE_CALENDAR_STRPTME_FMT_DT)

    def _to_python_date(self, google_calendar_date):
        return datetime.strptime(google_calendar_date, GOOGLE_CALENDAR_STRPTME_FMT)


class Event:

    def __init__(self, event_id, name, description, start, end, calendar, all_day=False, source_url=None,
                 timezone='America/New_York'):
        self.event_id = event_id
        self.name = name
        self.description = description

        self.all_day = all_day
        self.start = start
        self.end = end
        self.timezone = timezone

        self.source_url = source_url
        self.calendar = calendar

    def serialize(self):
        return {
            'description': self.description,
            'end': self.end.strftime('%Y-%m-%dT%H:%M:%S'),
            'source': {
                'title': 'Notion Link',
                'url': self.source_url,
            },
            'start': self.start.strftime('%Y-%m-%dT%H:%M:%S'),
            'summary': self.name,
            'timezone': self.timezone,
        }