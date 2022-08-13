import settings.config as config
from classes.calendar import Calendar

from services.google import GoogleService

google_service = GoogleService()

default_calendar = Calendar(
    config.DEFAULT_CALENDAR_NAME,
    config.DEFAULT_CALENDAR_ID,
)

default_calendar_event_data = google_service.get_calendar_event_data(default_calendar.calendar_id).get('items')
default_calendar.initialize_events(default_calendar_event_data)

for event in default_calendar.events:
    print(event)


# clean up
for event in default_calendar.events:
    del event

del default_calendar
