from Search_Venues_API_wrapper import single_restaurant
from Search_Venues_API_wrapper import all_restaurants
from Search_Venues_API_wrapper import all_restaurants_city
from Search_Venues_API_wrapper import search_by_theme
from rich import print
from datetime import datetime


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

    # Searching availability

    @staticmethod
    def search_availability_city_by_theme(date, hour, seats, city, theme):
        results = [single_restaurant(date, hour, seats, res) for res in
                   Multi_venue.get_all_restaurants_city_by_theme(city, theme)]
        # If method==seat restaurant has slots available
        results_availability = [restaurant for restaurant in results if restaurant['method'] == 'seat']
        return results_availability

    @staticmethod
    def search_availability_city(date, hour, seats, city):
        results = [single_restaurant(date, hour, seats, res) for res in Multi_venue.get_all_restaurants_city(city)]
        results_availability = [restaurant for restaurant in results if restaurant['method'] == 'seat']
        return results_availability

    @staticmethod
    def get_all_restaurants_available(date, hour, seats, venue_id=None):
        if venue_id is None:
            all_res = Multi_venue.get_all_restaurants()
        else:
            all_res = venue_id
        results = [single_restaurant(date, hour, seats, res) for res in all_res]
        results_availability = [restaurant for restaurant in results if restaurant['method'] == 'seat']
        return results_availability

    # TODO: add search hour range by city
    # TODO: remove search hour range of all restaurants
    @staticmethod
    def search_hour_range(date, seats, start_hour, last_hour, venue_id=None):
        results = [Multi_venue.get_all_restaurants_available(date, hour, seats, venue_id) for hour in
                   range(start_hour, last_hour + 100, 100)]
        return results

    @staticmethod
    def search_all_day(date, seats, venue_id=None):
        return Multi_venue.search_hour_range(date, seats, 0000, 2400, venue_id)

    @staticmethod
    def search_date_range(first, last, hour, seats, venue_id=None):
        results = [Multi_venue.get_all_restaurants_available(date, hour, seats, venue_id) for date in
                   range(first, last + 1, 1)]
        return results

    @staticmethod
    def print(list_of_availability):
        for i in range(len(list_of_availability)):
            for j in range(len(list_of_availability[i]['areas'])):
                if list_of_availability[i]['areas'][j]['options'][j]['method'] == 'seat':
                    print(list_of_availability[i]['areas'][j]['options'])


if __name__ == '__main__':
    res = Multi_venue.get_all_restaurants_available(20211122, 1800, 2,
                                                    ['junowine', 'yaffotelaviv', 'cafepopularrest', 'silo'])
    Multi_venue.print(res)
