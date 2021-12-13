import google_calendar_api_wrapper
from search_venues_API_wrapper import single_restaurant
from google_calendar_api_wrapper import CalenderView
from google_calendar_API import *
from rich import print
from datetime import datetime
from datetime import timedelta
import time


class SingleVenue:
    def __init__(self):
        pass

    # When is date time
    @staticmethod
    def availability(venue_id, seats, when):
        return single_restaurant(when, seats, venue_id)

    @staticmethod
    def add_to_calender(rest_id, seats, date, availability_slots):
        availability = {}
        new_calender = google_calendar_api_wrapper.CalenderView.add_calendar(rest_id)
        for key, value in availability_slots.items():
            for hour in value:
                if hour not in availability.keys():
                    availability[hour] = [key]
                else:
                    availability[hour] += [key]

        for key, value in availability.items():
            if len(key) == 4:
                new_date = date + timedelta(hours=int(key[:2]), minutes=int(key[2:]))
                google_calendar_api_wrapper.CalenderView.add_event(new_date, rest_id, seats, value,
                                                               new_calender)
        return new_calender

    @staticmethod
    def search_range_of_hours(venue_id, seats, when_start, when_end, frequency=60):
        date = when_start.replace(hour=00, minute=00)
        availability = single_restaurant(when_start, seats, venue_id)
        while when_start <= when_end:
            for key, value in single_restaurant(when_start, seats, venue_id).items():
                if isinstance(value, list):
                    if key in availability.keys():
                        availability[key] += value
                    else:
                        availability[key] = value
                elif isinstance(value, str):
                    if key in availability.keys():
                        availability[key] += [value]
                    else:
                        availability[key] = [value]
            when_start += timedelta(minutes=frequency)
        SingleVenue.add_to_calender(venue_id, seats, date, availability)
        return availability

    @staticmethod
    def search_day(venue_id, seats, when):
        date_hour_start = when + timedelta(hours=8)
        date_hour_end = when + timedelta(hours=24)
        return SingleVenue.search_range_of_hours(venue_id, seats, date_hour_start, date_hour_end, 60)

    @staticmethod
    def search_date_range(venue_id, seats, date, last_date):
        availability_slots = {}
        while date <= last_date:
            availability_slots[date.strftime("%m/%d/%Y")] = [SingleVenue.search_day(venue_id, seats, date)]
            date = date + timedelta(days=1)
        return availability_slots


if __name__ == '__main__':
    start = time.time()
    date_time_start = datetime.strptime("18/01/2022", '%d/%m/%Y')
    # availability = SingleVenue.search_range_of_hours('junowine', 3, "18/01/2022 17:00", "18/01/2022 21:00")
    date_time_end = datetime.strptime("18/01/2022 18:00", '%d/%m/%Y %H:%M')
    # , "18/01/2022 21:00"
    # print(SingleVenue.add_to_calender('junowine', 3, date_time_start, availability))
    print(SingleVenue.search_day('junowine', 3, date_time_start))
    end = time.time()
    print(end - start)
