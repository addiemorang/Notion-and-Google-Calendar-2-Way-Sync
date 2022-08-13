from notion_client import Client

from config import NOTION_TOKEN


class NotionService:
    """
    service class for communicating with notion
    """
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
        )
        self.pages = db_pages

        event_ids = []
        for page in db_pages:
            event_ids.append(page['properties'][self.EVENT_ID_PROPERTY]['rich_text'][0]['text']['content'])

        return event_ids
