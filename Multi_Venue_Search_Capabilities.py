from Search_Venues_API_wrapper import single_restaurant
from Search_Venues_API_wrapper import all_restaurants
from Search_Venues_API_wrapper import all_restaurants_city
from Search_Venues_API_wrapper import search_by_theme
from Search_Venues_API_wrapper import cities
from Search_Venues_API_wrapper import themes
from rich import print
from datetime import datetime
from datetime import timedelta


class Multi_venue:
    def __init__(self):
        pass

    @staticmethod
    def get_all_restaurants():
        restaurants = all_restaurants()
        all_venues = [restaurants[i]['pageId'] for i in range(len(restaurants))]
        return all_venues

    @staticmethod
    def get_all_restaurants_city(city):
        restaurants = all_restaurants_city(city)
        all_venues = [restaurants['venues'][i]['pageId'] for i in range(len(restaurants['venues']))]
        return all_venues

    @staticmethod
    def get_all_restaurants_city_by_theme(city, theme):
        restaurants = search_by_theme(city, theme)
        all_venues = [restaurants['venues'][i]['pageId'] for i in range(len(restaurants['venues']))]
        return all_venues

    @staticmethod
    def search_availability_city_by_theme(city, theme, seats, when):
        results = {}
        all_cities = [key for key in cities().keys()]
        all_themes = [key for key in themes().keys()]
        if city in all_cities and theme in all_themes:
            for res in Multi_venue.get_all_restaurants_city_by_theme(city, theme):
                results[res] = single_restaurant(when, seats, res)
            return results
        elif city in all_cities:
            print("The theme you choose is not in the list of themes, please choose another theme from the list: "
                  + str(all_themes))
        elif theme in all_themes:
            print("The city you choose is not in the list of cities, please choose another city from the list: "
                  + str(all_cities))
        else: print("The city and theme you choose is not in the list of cities/themes, please choose another city "
                    "and theme from the list: \n"
                  + "List of cities:" + str(all_cities) + "\n"
                    + "List of themes:" + str(all_themes))

    @staticmethod
    def search_availability_city(city, seats, when):
        results = {}
        all_cities = [key for key in cities().keys()]
        if city in all_cities:
            for res in Multi_venue.get_all_restaurants_city(city):
                results[res] = single_restaurant(when, seats, res)
        else: print("The city you choose is not in the list of cities, please choose another city from the list: " + str(all_cities))
        return results

    @staticmethod
    def get_all_restaurants_available(when, seats, venue_id=None):
        results = {}
        if venue_id is None:
            all_res = Multi_venue.get_all_restaurants()
        else:
            all_res = venue_id
        for res in all_res:
            results[res] = single_restaurant(when, seats, res)
        return results

    @staticmethod
    def search_hour_range_by_city(city, seats, when_start, when_end, frequency):
        availability_slots = {}
        all_cities = [key for key in cities().keys()]
        if city in all_cities:
            while when_start <= when_end:
                for key, value in Multi_venue.search_availability_city(city, seats, when_start).items():
                    availability_slots[key] = value
                when_start = when_start + timedelta(minutes=frequency)
        else: print("The city you choose is not in the list of cities, please choose another city from the list: " + str(all_cities))
        return availability_slots

    @staticmethod
    def search_hour_range_all_res(seats, when_start, when_end, frequency, venue_id=None):
        availability_slots = {}
        while when_start <= when_end:
            for key, value in Multi_venue.get_all_restaurants_available(when_start, seats, venue_id).items():
                availability_slots[key] = value
            when_start = when_start + timedelta(minutes=frequency)
        return availability_slots

    @staticmethod
    def search_multi_res_all_day(seats, when, venue_id=None):
        date_hour_start = when + timedelta(hours=10)
        date_hour_end = when + timedelta(hours=20)
        return Multi_venue.search_hour_range_all_res(seats, date_hour_start, date_hour_end, 60, venue_id)

    @staticmethod
    def search_all_day_by_city(seats, when, city):
        date_hour_start = when + timedelta(hours=12)
        date_hour_end = when + timedelta(hours=20)
        return Multi_venue.search_hour_range_by_city(city, seats, date_hour_start, date_hour_end, 60)

    @staticmethod
    def search_date_range(seats, when_start, when_end, venue_id=None):
        availability_slots = {}
        while when_start <= when_end:
            availability_slots[when_start.strftime("%m/%d/%Y")] = \
                Multi_venue.search_multi_res_all_day(seats, when_start, venue_id)
            when_start = when_start + timedelta(days=1)
        return availability_slots


if __name__ == '__main__':
    date_time = datetime.strptime(input("please enter the start date"), '%d/%m/%Y')
    date_time_end = datetime.strptime(input("please enter the end date"), '%d/%m/%Y')
    rest = ['junowine', 'yaffotelaviv', 'cafepopularrest', 'silo']
    print(Multi_venue.search_date_range(2, date_time, date_time_end, rest))
    # print(Multi_venue.search_availability_city('Jerusalem', 2, date_time))
