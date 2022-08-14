import settings.config as config
from classes.calendar import Calendar

from services.google import GoogleService
from services.notion import NotionService

google_service = GoogleService()
notion_service = NotionService()

default_calendar = Calendar(
    config.DEFAULT_CALENDAR_NAME,
    config.DEFAULT_CALENDAR_ID,
    config.DATABASE_ID,
)

notion_event_ids = notion_service.get_event_ids(config.DATABASE_ID)

default_calendar_event_data = google_service.get_calendar_event_data(default_calendar.calendar_id).get('items')
default_calendar.initialize_events(default_calendar_event_data)

for event in default_calendar.events:
    if event.event_id not in notion_event_ids:
        notion_service.create_event(event)


# clean up
for event in default_calendar.events:
    del event

del default_calendar
