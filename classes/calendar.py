from datetime import datetime

from constants import GOOGLE_CALENDAR_STRPTME_FMT, GOOGLE_CALENDAR_STRPTME_FMT_DT


class Calendar(object):

    def __init__(self, name, calendar_id, database_id):
        self.name = name
        self.calendar_id = calendar_id
        self.database_id = database_id

        self.events = []

    def initialize_events(self, event_data, notion_event_ids=None):
        for event in event_data:
            event_start = event['start']
            event_end = event['end']
            if 'dateTime' in event_start.keys() and 'dateTime' in event_end.keys():
                start = self._to_python_datetime(event['start']['dateTime'])
                end = self._to_python_datetime(event['end']['dateTime'])
                all_day = False
            else:
                start = self._to_python_date(event['start']['date'])
                end = self._to_python_date(event['end']['date'])
                all_day = True

            event_kwargs = {
                'all_day': all_day,
                'name': event['summary'],
                'calendar': self,
                'start': start,
                'end': end,
                'event_id': event['id'],
                'description': event.get('description', None)
            }

            new_event = Event(**event_kwargs)
            self.events.append(new_event)

    def _to_python_datetime(self, google_calendar_datetime):
        return datetime.strptime(google_calendar_datetime[:-6], GOOGLE_CALENDAR_STRPTME_FMT_DT)

    def _to_python_date(self, google_calendar_date):
        return datetime.strptime(google_calendar_date, GOOGLE_CALENDAR_STRPTME_FMT)

    def __str__(self):
        return self.name


class Event(object):

    def __init__(self, event_id, name, description, start, end, calendar, all_day, source_url=None,
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

    def __str__(self):
        return self.name
