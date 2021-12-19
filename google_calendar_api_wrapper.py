from google_calendar_API import *
from datetime import datetime
from datetime import timedelta
from restaurant_schedule_api import  *


class CalenderView:
    def __init__(self):
        pass

    @staticmethod
    def get_upcoming_events(calender_id=None):
        service = get_calendar_service(['https://www.googleapis.com/auth/calendar'])
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        if calender_id is None:
            events_result = service.events().list(calendarId='primary', timeMin=now,
                                                  maxResults=10, singleEvents=True,
                                                  orderBy='startTime').execute()
        else:
            events_result = service.events().list(calendarId=calender_id, timeMin=now,
                                                  maxResults=10, singleEvents=True,
                                                  orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    @staticmethod
    def get_all_calender_list(calender_id=None):
        service = get_calendar_service('https://www.googleapis.com/auth/calendar')
        # Call the Calendar API
        print('Getting list of calendars')
        calendars_result = service.calendarList().list().execute()

        calendars = calendars_result.get('items', [])
        if not calendars:
            print('No calendars found.')
        if calender_id is None:
            for calendar in calendars:
                summary = calendar['summary']
                id = calendar['id']
                primary = "Primary" if calendar.get('primary') else ""
                print("%s\t%s\t%s" % (summary, id, primary))
        else:
            for calendar in calendars:
                summary = calendar['summary']
                if calendar['id'] == calender_id:
                    primary = "Primary" if calendar.get('primary') else ""
                    print("%s\t%s\t%s" % (summary, calender_id, primary))

    @staticmethod
    def add_event(when, restaurant_id, seats, where_we_seat, calendar_id="7bpbgll4bos1al5e7ves65chl4@group.calendar.google.com"):
        service = get_calendar_service('https://www.googleapis.com/auth/calendar.events')
        start = when.isoformat()
        frequency = get_shifts(restaurant_id)
        end = (when + timedelta(minutes=frequency)).isoformat()
        event_result = service.events().insert(calendarId=calendar_id,
                                               body={
                                                   "summary": 'Reservation to: ' + restaurant_id + " for " +
                                                                  str(seats) + " seats",
                                                   "description": "Please choose where you want to seat: " + '\n'.join(where_we_seat),
                                                   "start": {"dateTime": start, "timeZone": 'Asia/Jerusalem'},
                                                   "end": {"dateTime": end, "timeZone": 'Asia/Jerusalem'},
                                               }
                                               ).execute()

        print("created event")
        # print("id: ", event_result['id'])
        print("summary: ", event_result['summary'])
        print("starts at: ", event_result['start']['dateTime'])
        print("ends at: ", event_result['end']['dateTime'])

    @staticmethod
    def add_calendar(restaurant_id):
        service = get_calendar_service(['https://www.googleapis.com/auth/calendar'])

        new_calendar = {
            'summary': str(restaurant_id),
            'timeZone': 'Asia/Jerusalem'
        }

        created_calendar = service.calendars().insert(body=new_calendar).execute()

        print("created_calendar")
        return created_calendar['id']


if __name__ == "__main__":
    pytopo_id = "7bpbgll4bos1al5e7ves65chl4@group.calendar.google.com"
    date = datetime.strptime("10/12/2021 10:30", '%d/%m/%Y %H:%M')
    # print(CalenderView.add_event(date, 'junowine', 4, 'בחוץ',))
    print(get_shifts('junowine'))
    # CalenderView.add_calendar('juno')
