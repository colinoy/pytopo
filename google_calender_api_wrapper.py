from google_calendar_API import *
from datetime import datetime
from datetime import timedelta


class CalenderView:
    def __init__(self):
        pass

    @staticmethod
    def get_upcoming_events(calender_id=None):
        service = get_calendar_service()
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
        service = get_calendar_service()
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
    def add_event(when, resturant_name, calendar_id="7bpbgll4bos1al5e7ves65chl4@group.calendar.google.com"):
        service = get_calendar_service()

        d = when
        start = when.isoformat()
        end = (when + timedelta(hours=2)).isoformat()

        event_result = service.events().insert(calendarId=calendar_id,
                                               body={
                                                   "summary": 'Automating calendar',
                                                   "description": 'This is a tutorial example of automating google calendar with python',
                                                   "start": {"dateTime": start, "timeZone": 'Asia/Kolkata'},
                                                   "end": {"dateTime": end, "timeZone": 'Asia/Kolkata'},
                                               }
                                               ).execute()

        print("created event")
        print("id: ", event_result['id'])
        print("summary: ", event_result['summary'])
        print("starts at: ", event_result['start']['dateTime'])
        print("ends at: ", event_result['end']['dateTime'])


if __name__ == "__main__":
    pytopo_id = "7bpbgll4bos1al5e7ves65chl4@group.calendar.google.com"
    date = datetime.strptime("10/12/2021 10:30", '%d/%m/%Y %H:%M')
    CalenderView.add_event(date, 'juno')
