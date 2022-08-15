# Notion-and-Google-Calendar-2-Way-Sync

See [original repo](https://github.com/akarri2001/Notion-and-Google-Calendar-2-Way-Sync for) for extra info.

## Setup

The setting directory should house
    - your client secret JSON file
    - your token.pkl file
    - a python file named `config.py`

In `config.py`, copy and paste the following:
```python
# Notion database info
DATABASE_ID = ''

DEFAULT_CALENDAR_ID = ''

DEFAULT_CALENDAR_NAME = ''

# Auth token from Notion (see original repo for more info)
NOTION_TOKEN = ''

PROJECT_PATH = '/Users/<your-computer-user>/notion/notion_gcal_sync/'

CREDS_PATH = f'{PROJECT_PATH}settings/token.pkl'

# Root URL of your Notion database (see original repo for more info)
ROOT_URL = ''
```

None of these files (client secret, token.pkl, or config.py) should ever be shared or made public. 
All of these are listed in .gitignore which should keep them from being committed automatically,
but please always double-check before committing and pushing to github.

## Program
You're going to need to do much of the setup described in the 
[instructions doc](https://docs.google.com/document/d/1uP-6EsmTlG_Gttg9jC0MBZKHpjccVapIeC1D1tR1yXc/edit)

To run the program, in your terminal, run `cd /notion/notion_gcal_sync/` and then run `python3 sync_v2.py`.

V2 is a refactored version of `sync.py` which is just nearly identical to the original script 
`Notion-GCal-2WaySync-Public.py`.

- V2 currently only refactors the Google Calendar to Notion sync, Notion to Google Calendar sync is to come
- V2 handles some cases of recurring events
- V2 needs test coverage