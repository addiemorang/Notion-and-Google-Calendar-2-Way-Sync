import re

from datetime import date, datetime, timedelta

from constants import GOOGLE_CALENDAR_STRPTME_FMT, GOOGLE_CALENDAR_STRPTME_FMT_DT, GOOGLE_CALENDAR_WEEKDAYS


class Calendar(object):

    def __init__(self, name, calendar_id, database_id):
        self.name = name
        self.calendar_id = calendar_id
        self.database_id = database_id

        self.events = []

    def initialize_events(self, event_data):
        for event in event_data:

            # configure start and end dates
            event_start = event['start']
            event_end = event['end']
            if 'dateTime' in event_start.keys() and 'dateTime' in event_end.keys():
                event_start = event['start']['dateTime']
                event_end = event['end']['dateTime']
                all_day = False
            else:
                event_start = event['start']['date']
                event_end = event['end']['date']
                all_day = True

            if not all_day:
                event_start = self._to_python_datetime(event_start)
                event_end = self._to_python_datetime(event_end)
            else:
                event_start = self._to_python_date(event_start)
                event_end = self._to_python_date(event_end)

            recurring = 'recurrence' in event.keys()

            if recurring:
                recurrence_list = event['recurrence']
                recurrence_fields = self._parse_recurrence_fields(recurrence_list)

                if recurrence_fields['exception_days']:
                    # TODO test this
                    if event_start in recurrence_fields['exception_days']:
                        continue

                if recurrence_fields['weekday']:
                    today = datetime.now().date()
                    today_weekday = today.weekday()
                    days_ahead = (recurrence_fields['weekday'] - today_weekday) % 7
                    event_start = datetime.combine(today + timedelta(days=days_ahead), event_start.time())
                    event_end = datetime.combine(today + timedelta(days=days_ahead), event_end.time())

            # configure description
            event_description = event.get('description', None)
            if not event_description:
                event_description = ''

            event_kwargs = {
                'all_day': all_day,
                'name': event['summary'],
                'calendar': self,
                'start': event_start,
                'end': event_end,
                'event_id': event['id'],
                'description': event_description
            }

            new_event = Event(**event_kwargs)
            self.events.append(new_event)

    def _parse_recurrence_fields(self, recurrence_list):
        # See https://www.rfc-editor.org/rfc/rfc5545#section-3.8.5
        exception_days = []
        frequency = None
        weekday = None

        for recurrence_field in recurrence_list:
            if recurrence_field.startswith('EXDATE'):
                search_result = re.search(r'(?P<exceptions>(?<=:)[\dT,]*)', recurrence_field).group('exceptions')
                matches = re.sub(r'T\d*', '', search_result)

                for match in matches.split(','):
                    year = int(match[:4])
                    month = int(match[4:6])
                    day = int(match[6:])
                    exception_days.append(date(year, month, day))
            elif recurrence_field.startswith('RRULE'):
                frequency = re.search(r'(?P<frequency>(?<=FREQ=)[A-Z]*)', recurrence_field).group('frequency')
                if frequency == 'WEEKLY':
                    # What should we use frequency for?
                    day = re.search(r'(?P<day>(?<=BYDAY=)[A-Z]*)', recurrence_field).group('day')
                    weekday = GOOGLE_CALENDAR_WEEKDAYS.index(day)

        return {
            'exception_days': exception_days,
            'frequency': frequency,
            'weekday': weekday,
        }
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
