from Search_Venues_API_wrapper import single_restaurant
from rich import print


class Single_venue:
    def __init__(self):
        pass

    @staticmethod
    def availability(date, hour, seats, venue_id):
        return single_restaurant(date, hour, seats, venue_id)

    @staticmethod
    def Search_Range_of_Hours(date, seats, venue_id, start, stop):
        availability_slots = [single_restaurant(date, hour, seats, venue_id) for hour in range(start, stop + 100, 100)]
        return availability_slots

    @staticmethod
    def search_day(date, seats, venue_id):
        availability_slots = [single_restaurant(date, hour, seats, venue_id) for hour in range(0000, 2500, 100)]
        return availability_slots

    @staticmethod
    def Search_Date_Range(seats, venue_id, hour, date, last_date):
        availability_slots = [single_restaurant(data, hour, seats, venue_id) for data in range(date, last_date, 1)]
        return availability_slots


print(Single_venue.availability(20211119, 1800, 2, 'junowine'))
