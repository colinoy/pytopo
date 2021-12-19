import google_calendar_api_wrapper
from search_venues_API_wrapper import single_restaurant
from restaurant_schedule_api import *
from rich import print
from datetime import datetime
from datetime import timedelta
import time


class SingleVenue:
    def __init__(self):
        pass

    '''
    When is date time
    '''

    @staticmethod
    def availability(venue_id, seats, when):
        return single_restaurant(when, seats, venue_id)

    @staticmethod
    def add_to_calender(rest_id, seats, date, availability_slots, calender=None):
        availability = {}
        if calender is None:
            new_calender = google_calendar_api_wrapper.CalenderView.add_calendar(rest_id)
        else: new_calender = calender
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
    def search_range_of_hours(venue_id, seats, when_start, when_end, frequency=60, calender=None):
        date = when_start.replace(hour=00, minute=00)
        availability = single_restaurant(when_start, seats, venue_id)
        for key, value in availability.items():
            if isinstance(value, str):
                availability[key] = [value]
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
        SingleVenue.add_to_calender(venue_id, seats, date, availability, calender)
        return availability

    @staticmethod
    def search_day(venue_id, seats, when, calender=None):
        restaurants_schedule = get_restaurant_schedule_for_day(venue_id, when)
        hours = list(restaurants_schedule.keys())
        date_hour_start = datetime.combine(when, hours[0])
        date_hour_end = datetime.combine(when, hours[len(restaurants_schedule) - 1])
        return SingleVenue.search_range_of_hours(venue_id, seats, date_hour_start, date_hour_end, 60, calender)

    @staticmethod
    def search_date_range(venue_id, seats, date, last_date):
        availability_slots = {}
        new_calender = google_calendar_api_wrapper.CalenderView.add_calendar(venue_id)
        while date <= last_date:
            availability_slots[date] = [SingleVenue.search_day(venue_id, seats, date, new_calender)]
            date = date + timedelta(days=1)
        return availability_slots


if __name__ == '__main__':
    start = time.time()
    date_time_start = datetime.strptime("18/01/2022", '%d/%m/%Y')
    # availability = SingleVenue.search_range_of_hours('junowine', 3, "18/01/2022 17:00", "18/01/2022 21:00")
    date_time_end = datetime.strptime("18/01/2022 18:00", '%d/%m/%Y %H:%M')
    # , "18/01/2022 21:00"
    # print(SingleVenue.add_to_calender('junowine', 3, date_time_start, availability))
    # print(SingleVenue.search_day('junowine', 3, date_time_start))
    print(SingleVenue.search_date_range('junowine', 2, datetime.strptime("18/01/2022", '%d/%m/%Y'),
                                        datetime.strptime("19/01/2022", '%d/%m/%Y')))
    end = time.time()
    print(end - start)
