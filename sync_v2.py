import os
import pickle

from calendar import Calendar
from services.google import GoogleService
from config import CREDS_PATH, DATABASE_ID, DEFAULT_CALENDAR_ID, NOTION_TOKEN, ROOT_URL
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from notion_client import Client

google_service = GoogleService()

default_calendar_resource = google_service.get_calendar_resource(DEFAULT_CALENDAR_ID)

Calendar()
