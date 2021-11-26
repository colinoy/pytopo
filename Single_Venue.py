from Search_Venues_API_wrapper import single_restaurant
from rich import print
from datetime import datetime
from datetime import timedelta


class SingleVenue:
    def __init__(self):
        pass

    @staticmethod
    def availability(venue_id, seats, when):
        date_time = datetime.strptime(when, '%d/%m/%Y  %H:%M')
        return single_restaurant(date_time, seats, venue_id)

    @staticmethod
    def search_range_of_hours(venue_id, seats, when_start, when_end, frequency):
        date_time_start = datetime.strptime(when_start, '%d/%m/%Y  %H:%M')
        date_time_end = datetime.strptime(when_end, '%d/%m/%Y  %H:%M')
        availability_slots = {}
        while date_time_start <= date_time_end:
            for key, value in single_restaurant(date_time_start, seats, venue_id).items():
                if key in availability_slots.keys():
                    availability_slots[key] += value
                else: availability_slots[key] = value
            date_time_start += timedelta(minutes=frequency)
        for key, value in availability_slots.items():
            availability_slots[key] = sorted(set(value))
        return availability_slots

    @staticmethod
    def search_day(venue_id, seats, when):
        date_time = datetime.strptime(when, '%d/%m/%Y') + timedelta(hours=0)
        hours = 1
        availability_slots = {}
        while hours < 24:
            for key, value in single_restaurant(date_time, seats, venue_id).items():
                if key in availability_slots.keys():
                    availability_slots[key] += value
                else:
                    availability_slots[key] = value
            hours += 1
            date_time += timedelta(hours=hours)
        for key, value in availability_slots.items():
            availability_slots[key] = sorted(set(value))
        return availability_slots

    @staticmethod
    def search_date_range(venue_id, seats, date, last_date):
        availability_slots = [SingleVenue.search_day(data, seats, venue_id) for data in range(date, last_date, 1)]
        return availability_slots


if __name__ == '__main__':
    print(SingleVenue.search_day('junowine', 2, "13/12/2021"))
