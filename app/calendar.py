class Event:

    def __init__(self, name, description, start, end, source_url, calendar_id, all_day=False,
                 timezone='America/New_York'):
        self.name = name
        self.description = description

        self.all_day = all_day
        self.start = start
        self.end = end
        self.timezone = timezone

        self.source_url = source_url
        self.calendar_id = calendar_id

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
