from Search_Venues_API_wrapper import single_restaurant
from Search_Venues_API_wrapper import all_restaurants
from Search_Venues_API_wrapper import all_restaurants_city
from rich import print


class Multi_venue():
    def __init__(self, date, hour, seats, venues=[]):
        self.date = date
        self.hour = hour
        self.seats = seats
        self.venues = venues
        self.all_availabe = []

    def get_all_restaurants(self):
        if len(self.venues) == 0 and self.city == '':
            restaurants = all_restaurants()
            self.venues = [restaurants[i]['pageId'] for i in range(0, len(all_restaurants()))]
        if len(self.venues) == 0 and self.city != '':
            restaurants = all_restaurants_city()
            self.venues = [restaurants[i]['pageId'] for i in range(0, len(all_restaurants_city()))]
        return self.venues

    def get_all_restaurants_available(self):
        results = [single_restaurant(self.date, self.hour, self.seats, res) for res in self.get_all_restaurants()]
        for restaurant in results:
            if restaurant['method'] == 'seat':
                self.all_availabe.append(restaurant)
        return self.all_availabe

    def search_hour_range(self, start_hour, last_hour):
        results = []
        for hour in range(start_hour, last_hour + 100, 100):
            results = [single_restaurant(self.date, hour, self.seats, res) for res in self.get_all_restaurants()]
        return results

    def search_all_day(self):
        return self.search_hour_range(0000, 2400)

    def search_date_range(self, first, last):
        results = []
        for day in range(first, last + 1, 1):
            results = [single_restaurant(day, self.hour, self.seats, res) for res in self.get_all_restaurants()]
        return results



test1 = Multi_venue(20211122, 1800, 2,
                    ['yaffotelaviv', 'cafepopularrest', 'silo', 'cafeeuropa', 'dixie', 'thebluerooster'])
print(test1.search_date_range(20211122, 20211123))

