from Search_Venues_API_wrapper import single_restaurant
from rich import print


class Single_venue:
    def __init__(self, date, hour, seats, venue_id):
        self.date = date
        self.hour = hour
        self.seats = seats
        self.venue_id = venue_id

    def availability(self):
        return single_restaurant(self.date, self.hour, self.seats, self.venue_id)

    def Search_Range_of_Hours(self, start, stop):
        availability_slots = []
        for hour in range(start, stop + 100, 100):
            availability_slots.append(single_restaurant(self.date, hour, self.seats, self.venue_id))
        return availability_slots



str343 = Single_venue(20211117, 1800, 3, "junowine")
print(str343.Search_Range_of_Hours(1700, 2000))
