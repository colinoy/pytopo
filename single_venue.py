import google_calendar_api_wrapper
from search_venues_API_wrapper import single_restaurant
from google_calendar_api_wrapper import CalenderView
from rich import print
from datetime import datetime
from datetime import timedelta
import time


class SingleVenue:
    def __init__(self):
        pass

    @staticmethod
    def availability(venue_id, seats, when):
        date_time = datetime.strptime(when, '%d/%m/%Y  %H:%M')
        availability_slots = single_restaurant(date_time, seats, venue_id)
        availability = {}
        new_calender = google_calendar_api_wrapper.CalenderView.add_calendar(venue_id)
        for key, value in availability_slots.items():
            for hour in value:
                if hour not in availability.keys():
                    availability[hour] = [key]
                else: availability[hour] += [key]
        for key, value in availability.items():
            date = when[:11] + key
            date_time = datetime.strptime(date, '%d/%m/%Y  %H%M')
            where_we_seats = value
            google_calendar_api_wrapper.CalenderView.add_event(date_time, venue_id, seats, where_we_seats, new_calender['id'])
        return availability

    @staticmethod
    def search_range_of_hours(venue_id, seats, when_start, when_end, frequency):
        availability_slots = {}
        while when_start <= when_end:
            for key, value in single_restaurant(when_start, seats, venue_id).items():
                if isinstance(value, list):
                    if key in availability_slots.keys():
                        availability_slots[key] += value
                    else:
                        availability_slots[key] = value
                elif isinstance(value, str):
                    if key in availability_slots.keys():
                        availability_slots[key] += [value]
                    else:
                        availability_slots[key] = [value]
            when_start += timedelta(minutes=frequency)
        for key, value in availability_slots.items():
            availability_slots[key] = sorted(set(value))
        return availability_slots

    @staticmethod
    def search_day(venue_id, seats, when, start_hour=0, end_hour=24):
        date_hour_start = when + timedelta(hours=start_hour)
        date_hour_end = when + timedelta(hours=end_hour)
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
    # date_time_start = datetime.strptime("13/12/2021 17:00")
    # date_time_end = datetime.strptime("23/12/2021", '%d/%m/%Y')
    print(SingleVenue.availability('junowine', 2, "23/01/2022 19:00"))
    end = time.time()
    print(end - start)
