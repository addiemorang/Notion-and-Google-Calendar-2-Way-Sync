import logging
from datetime import datetime

from notion_client import Client

from settings.config import NOTION_TOKEN


class NotionService:
    '''
    service class for communicating with notion
    '''
    TASK_PROPERTY = 'Task Name'
    DATE_PROPERTY = 'Date'
    INITIATIVE_PROPERTY = 'Initiative'
    EXTRA_INFO_PROPERTY = 'Extra Info'
    ON_GCAL_PROPERTY = 'On GCal?'
    NEED_UPDATE_PROPERTY = 'NeedGCalUpdate'
    EVENT_ID_PROPERTY = 'GCal Event Id'
    LAST_UPDATED_PROPERTY = 'Last Updated Time'
    CALENDAR_PROPERTY = 'Calendar'
    CURRENT_CALENDAR_ID_PROPERTY = 'Current Calendar Id'
    DELETE_PROPERTY = 'Done?'

    def __init__(self):
        self.client = Client(auth=NOTION_TOKEN)
        self.pages = None

    def create_event(self, event):
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S-04:00')

        kwargs = {
            'parent': {
                'database_id': event.calendar.database_id,
            },
            'properties': {
                self.TASK_PROPERTY: {
                    'type': 'title',
                    'title': [
                        {
                            'type': 'text',
                            'text': {
                                'content': event.name,
                            },
                        },
                    ],
                },
                self.LAST_UPDATED_PROPERTY: {
                    'type': 'date',
                    'date': {
                        'start': now,
                        'end': None,
                    }
                },
                self.EXTRA_INFO_PROPERTY: {
                    'type': 'rich_text',
                    'rich_text': [{
                        'text': {
                            'content': event.description,
                        }
                    }]
                },
                self.EVENT_ID_PROPERTY: {
                    'type': 'rich_text',
                    'rich_text': [{
                        'text': {
                            'content': event.event_id
                        }
                    }]
                },
                self.ON_GCAL_PROPERTY: {
                    'type': 'checkbox',
                    'checkbox': True
                },
                self.CURRENT_CALENDAR_ID_PROPERTY: {
                    'rich_text': [{
                        'text': {
                            'content': event.calendar.calendar_id,
                        }
                    }]
                },
                self.CALENDAR_PROPERTY: {
                    'select': {
                        'name': event.calendar.name,
                    },
                },
            },
        }

        if event.all_day:
            days_between = event.end-event.start
            if days_between.days == 1:
                kwargs['properties'].update({
                    self.DATE_PROPERTY: {
                        'type': 'date',
                        'date': {
                            'start': event.start.strftime('%Y-%m-%d'),
                            'end': None,
                        }
                    }
                })
            else:
                kwargs['properties'].update({
                    self.DATE_PROPERTY: {
                        'type': 'date',
                        'date': {
                            'start': event.start.strftime('%Y-%m-%d'),
                            'end': event.end.strftime('%Y-%m-%d'),
                        }
                    }
                })
        else:
            kwargs['properties'].update({
                self.DATE_PROPERTY: {
                    'type': 'date',
                    'date': {
                        'start': event.start.strftime('%Y-%m-%dT%H:%M:%S-04:00'),
                        'end': event.end.strftime('%Y-%m-%dT%H:%M:%S-04:00'),
                    }
                }
            })

        self.client.pages.create(**kwargs)

        logging.info(f'Created event {event.name} in Notion')

    def get_event_ids(self, database_id):
        db_pages = self.client.databases.query(
            **{
                'database_id': database_id,
                'filter': {
                    'property': self.EVENT_ID_PROPERTY,
                    'text': {
                        'is_not_empty': True
                    },
                },
            }
        ).get('results')
        self.pages = db_pages

        event_ids = []
        for page in db_pages:
            event_ids.append(page['properties'][self.EVENT_ID_PROPERTY]['rich_text'][0]['text']['content'])

        return event_ids
