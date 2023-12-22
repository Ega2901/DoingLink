from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from redisdb import *
import datetime
import os
def build_google_calendar_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/calendar.readonly'])
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', ['https://www.googleapis.com/auth/calendar.readonly'])
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service

def get_google_calendar_events():
    try:
        service = build_google_calendar_service()

        now = datetime.datetime.utcnow().isoformat() + 'Z'
        end_of_day = datetime.datetime.now().replace(hour=23, minute=59, second=59).isoformat() + 'Z'

        events_result = (
            service.events()
            .list(
                calendarId='primary',
                timeMin=now,
                timeMax=end_of_day,
                maxResults=10,
                singleEvents=True,
                orderBy='startTime',
            )
            .execute()
        )
        events = events_result.get('items', [])

        return events

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
    
def get_schedule_data():
    events = get_google_calendar_events()

    if not events:
        return None

    schedule_data = {"events": []}

    for event in events:
        start_time = event['start'].get('dateTime', event['start'].get('date'))
        end_time = event['end'].get('dateTime', event['end'].get('date'))
        event_name = event['summary']
        location = event.get('location', 'местоположение не указано')

        schedule_data['events'].append(
            {"start_time": start_time, "end_time": end_time, "event_name": event_name, "location": location}
        )

    return schedule_data

def send_schedule():
    schedule_data = get_schedule_data()

    if not schedule_data:
        return None

    # Check if there are any events
    if not schedule_data['events']:
        return None

    # Take only the first event
    event1 = schedule_data['events'][0]
    event2 = schedule_data['events'][1]

    date1 = event1['start_time'].split("T")[0][-2:] if 'start_time' in event1 else None
    date2 = event2['start_time'].split("T")[0][-2:] if 'start_time' in event2 else None
    if  date1 == date2:
            # Format the message with information about the event
        start_time1 = event1['start_time'].split("T")[1][:5] if 'start_time' in event1 else 'время не указано'
        end_time1 = event1['end_time'].split("T")[1][:5] if 'end_time' in event1 else 'время не указано'
        event_name1 = event1['event_name']
        location1 = event1['location']

        start_time2 = event2['start_time'].split("T")[1][:5] if 'start_time' in event2 else 'время не указано'
        end_time2 = event2['end_time'].split("T")[1][:5] if 'end_time' in event2 else 'время не указано'
        event_name2 = event2['event_name']
        location2 = event2['location']

        schedule_message = (
            f"Привет, ребят!\n\n"
            f"Сегодня у нас пары в {location1}\n"
            f"{start_time1}-{end_time1} - {event_name1}\n"
            f"{start_time2}-{end_time2} - {event_name2}\n"
            f"\nПросьба быть всех вовремя, к {start_time1}!\n"
            f"\nКто опоздает - shame!"
        )
    else:
        start_time = event1['start_time'].split("T")[1][:5] if 'start_time' in event1 else 'время не указано'
        end_time = event1['end_time'].split("T")[1][:5] if 'end_time' in event1 else 'время не указано'
        event_name = event1['event_name']
        location = event1['location']

        schedule_message = (
            f"Привет, ребят!\n\n"
            f"Сегодня у нас пары в {location}\n"
            f"{start_time}-{end_time} - {event_name}\n"
            f"\nПросьба быть всех вовремя, к {start_time}!\n"
            f"\nКто опоздает - shame!"
        )

    return schedule_message
    
