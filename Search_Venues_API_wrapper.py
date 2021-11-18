from rich import print
import requests
import json

cities = {"Tel Aviv": {"lat": 32.0650841, "lon": 34.7708837, "distance": 5},
          "Jerusalem": {"lat": 31.7664943, "lon": 35.2251867, "distance": 5},
          'Haifa': {"lat": 32.7889988, "lon": 34.9659817, "distance": 5},
          'Hashron': {"lat": 32.1786311, "lon": 34.9051415, "distance": 5},
          "Ashdod": {"lat": 31.800862, "lon": 34.633986, "distance": 5},
          "Eilat": {"lat": 29.5624557, "lon": 34.9592158, "distance": 5},
          "Beer Sheva": {"lat": 31.259107, "lon": 34.7971397, "distance": 5},
          "Ramat gan": {"lat": 32.0478643, "lon": 34.8160228, "distance": 5},
          "Modieen": {"lat": 31.9012745, "lon": 35.0028285, "distance": 5},
          "Rehovot": {"lat": 31.9110709, "lon": 34.8053529, "distance": 5},
          "Herzilia": {"lat": 32.1575675, "lon": 34.8325876, "distance": 5},
          "Rishon Lezion": {"lat": 31.9755346, "lon": 34.8089678, "distance": 5},
          "Netahnya": {"lat": 32.3302093, "lon": 34.8484746, "distance": 5},
          "Hedera": {"lat": 32.4424186, "lon": 34.8949194, "distance": 5},
          "Petah Tikva": {"lat": 32.09004, "lon": 34.8584, "distance": 5},
          "Holon": {"lat": 31.9302558, "lon": 34.7872933, "distance": 5},
          "Kineret": {"lat": 32.8525805, "lon": 35.6659112, "distance": 20}}

themes = {"meats": "\u05D1\u05E9\u05E8\u05D9\u05DD",
          "italian": "\u05D0\u05D9\u05D8\u05DC\u05E7\u05D9",
          "fish": "\u05D3\u05D2\u05D9\u05DD",
          "yam tichoni": "\u05D9\u05DD \u05EA\u05D9\u05DB\u05D5\u05E0\u05D9",
          "israeli": "\u05D9\u05E9\u05E8\u05D0\u05DC\u05D9",
          "American": "\u05D0\u05DE\u05E8\u05D9\u05E7\u05D0\u05D9",
          "Bistro": "\u05D1\u05D9\u05E1\u05D8\u05E8\u05D5",
          "Asian": "\u05D0\u05E1\u05D9\u05D9\u05EA\u05D9",
          "bar": "\u05D1\u05E8",
          "Food bar": "\u05D1\u05E8 \u05D0\u05D5\u05DB\u05DC",
          "Tapas": "\u05D8\u05D0\u05E4\u05D0\u05E1",
          "coffee": "\u05D1\u05D9\u05EA \u05E7\u05E4\u05D4",
          "Vegan": "\u05D8\u05D1\u05E2\u05D5\u05E0\u05D9",
          "meatless": "\u05E6\u05DE\u05D7\u05D5\u05E0\u05D9",
          "south American": "\u05D3\u05E8\u05D5\u05DD \u05D0\u05DE\u05E8\u05D9\u05E7\u05D0\u05D9",
          "Farm to table": "\u05DE\u05D4\u05D7\u05D5\u05D5\u05D4 \u05DC\u05E9\u05D5\u05DC\u05D7\u05DF",
          "Wine": "\u05D9\u05E7\u05D1",
          "Kosher": "\u05DB\u05E9\u05E8",
          "shushi": "\u05E1\u05D5\u05E9\u05D9",
          "Indian": "\u05D4\u05D5\u05D3\u05D9",
          "Vietnam": "\u05D5\u05D9\u05D0\u05D8\u05E0\u05DE\u05D9",
          "Japanese": "\u05D9\u05E4\u05E0\u05D9",
          "Chinese": "\u05E1\u05D9\u05E0\u05D9"}


def single_restaurant(date, time, size, restaurant_id):
    headers = {
        'authority': 'ontopo.co.il',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json;charset=UTF-8',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/95.0.4638.54 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'origin': 'https://ontopo.co.il',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://ontopo.co.il/arestauranttlv/',
        'accept-language': 'he,en-US;q=0.9,en;q=0.8',
        'cookie': '_ga=GA1.3.705025712.1624537679; _gcl_au=1.1.1553806650.1636522977; '
                  'auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
                  '.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsiYW5vbnltb3VzIl0sIngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6ImFub255bW91cyIsIngtaGFzdXJhLXVzZXItaWQiOiIwMWU3YWYxMi0xMjRjLTQ5YzYtYTg5Ni1mM2Y5MjU4MDU1MzIifSwiaWF0IjoxNjM2NTIyOTc2LCJleHAiOjE2MzY1MjM4NzZ9.b7QzocZUaSaKBoa1Yrp10UuJ6MrrybSHq7zN1Ie-42g; auth_refresh_token=e375b61a-f9e2-4e05-9bcd-53fc45e6151c; auth_token_expired=2021-11-10T05%3A52%3A56Z; _gid=GA1.3.1953460068.1636522980; _gat_UA-113921616-2=1',
    }

    data = {"page_id": str(restaurant_id), "locale": "he",
            "criteria": {"size": str(size), "date": str(date), "time": str(time)},
            "app": "web", "origin": "marketplace", "sessionId": "b760d78b-9e27-44d1-b4af-34fa0e2af28f",
            "stationId": "fd0f0464-1637-4baf-9aea-1821ecaa8d54", "sendAnalytics": "true"}

    response = requests.post('https://ontopo.co.il/api/availability/searchAvailability', headers=headers, json=data)
    response = response.json()
    return response


def all_restaurants_city(city):
    headers = {
        'authority': 'ontopo.co.il',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json;charset=UTF-8',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'origin': 'https://ontopo.co.il',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://ontopo.co.il/results/?region=%D7%AA%D7%9C%20%D7%90%D7%91%D7%99%D7%91&size=2&date=20211111&time=2000&market=4342499',
        'accept-language': 'he,en-US;q=0.9,en;q=0.8',
        'cookie': '_ga=GA1.3.705025712.1624537679; _gcl_au=1.1.1553806650.1636522977; _gid=GA1.3.1953460068.1636522980; auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsiYW5vbnltb3VzIl0sIngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6ImFub255bW91cyJ9LCJpYXQiOjE2MzY2MjMxMDQsImV4cCI6MTYzNjYyNDAwNH0.5jaUJY46V9Q8F7gQsEY7FQqe_Un5RzFV9GTjVT9Stno; auth_refresh_token=12475110-19f9-45cc-b29e-0f2a69bc5e45; auth_token_expired=2021-11-11T09%3A41%3A44Z; _gat_UA-113921616-2=1',
    }

    data = {"directory": "culinary.pages.il", "locale": "he",
            "filter": {"location": {"lat": cities[city]['lat'], "lon": cities[city]['lon']},
                       "distance": cities[city]["distance"],
                       "component": "reservation"},
            "size": 227, "search_after": "", "market": "XzW03HZwb"}

    response = requests.post('https://ontopo.co.il/api/results/searchVenues', headers=headers, json=data)
    response = response.json()
    return response


def all_restaurants():
    headers = {
        'authority': 'ontopo.co.il',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json;charset=UTF-8',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'origin': 'https://ontopo.co.il',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://ontopo.co.il/results/?region=%D7%AA%D7%9C%20%D7%90%D7%91%D7%99%D7%91&size=2&date=20211111&time=2000&market=4342499',
        'accept-language': 'he,en-US;q=0.9,en;q=0.8',
        'cookie': '_ga=GA1.3.705025712.1624537679; _gcl_au=1.1.1553806650.1636522977; _gid=GA1.3.1953460068.1636522980; auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsiYW5vbnltb3VzIl0sIngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6ImFub255bW91cyJ9LCJpYXQiOjE2MzY2MjMxMDQsImV4cCI6MTYzNjYyNDAwNH0.5jaUJY46V9Q8F7gQsEY7FQqe_Un5RzFV9GTjVT9Stno; auth_refresh_token=12475110-19f9-45cc-b29e-0f2a69bc5e45; auth_token_expired=2021-11-11T09%3A41%3A44Z; _gat_UA-113921616-2=1',
    }

    data = {"directory": "culinary.pages.il", "locale": "he",
            "filter": {"component": "reservation"},
            "size": 227, "search_after": "", "market": "XzW03HZwb"}

    response = requests.post('https://ontopo.co.il/api/results/searchVenues', headers=headers, json=data)
    response = response.json()
    return response['venues']


def search_by_theme(city, theme):
    import requests

    headers = {
        'authority': 'ontopo.co.il',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json;charset=UTF-8',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'origin': 'https://ontopo.co.il',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://ontopo.co.il/results/?region=%D7%AA%D7%9C%20%D7%90%D7%91%D7%99%D7%91&size=2&date=20211114&time=2000&market=4342499',
        'accept-language': 'he',
        'cookie': '_gcl_au=1.1.1683183408.1636663583; _ga=GA1.3.2084581254.1636663583; _fbp=fb.2.1636663584969.2003306758; _gid=GA1.3.385775143.1636894681; auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsiYW5vbnltb3VzIl0sIngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6ImFub255bW91cyJ9LCJpYXQiOjE2MzY4OTc4NzksImV4cCI6MTYzNjg5ODc3OX0.GvlQH-5WvWMPQwVvqHZgao3XLXWWtyNCiDLu4tm_Ep4; auth_refresh_token=1a340ed0-3f72-4991-9a1b-922f727407e0; auth_token_expired=2021-11-14T14%3A01%3A19Z; _gat_UA-113921616-2=1',
    }

    data = {"directory": "culinary.pages.il", "locale": "he", "filter": {"service": themes[theme],
                                                                         "location": {"lat": cities[city]['lat'],
                                                                                      "lon": cities[city]['lon']},
                                                                         "distance": cities[city]["distance"],
                                                                         "component": "reservation"}, "size": 280,
            "search_after": "", "market": "XzW03HZwb"}

    response = requests.post('https://ontopo.co.il/api/results/searchVenues', headers=headers, json=data)
    response = response.json()
    return response


# print(single_restaurant(20211121, 1800,2,'yaffotelaviv'))
