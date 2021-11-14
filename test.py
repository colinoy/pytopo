from rich import print
# import requests
#
# headers = {
#     'authority': 'ontopo.co.il',
#     'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
#     'accept': 'application/json, text/plain, */*',
#     'content-type': 'application/json;charset=UTF-8',
#     'sec-ch-ua-mobile': '?0',
#     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
#     'sec-ch-ua-platform': '"macOS"',
#     'origin': 'https://ontopo.co.il',
#     'sec-fetch-site': 'same-origin',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-dest': 'empty',
#     'referer': 'https://ontopo.co.il/junowine/',
#     'accept-language': 'he',
#     'cookie': '_gcl_au=1.1.1683183408.1636663583; _ga=GA1.3.2084581254.1636663583; _gid=GA1.3.641795585.1636663583; _fbp=fb.2.1636663584969.2003306758; auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsiYW5vbnltb3VzIl0sIngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6ImFub255bW91cyJ9LCJpYXQiOjE2MzY2NjQyMTAsImV4cCI6MTYzNjY2NTExMH0.XWCNEuFNPefXVs5Qjm1OCH1r0QpyaHqVaQ7FGCDmrs8; auth_refresh_token=c4394d8d-1a36-45eb-827c-a33dd403bb32; auth_token_expired=2021-11-11T21%3A06%3A50Z; _gat_UA-113921616-2=1',
# }
#
# data = {"page_id": "babayaga", "locale": "he", "criteria": {"size": "2", "date": "20211113", "time": "1900"},
#         "app": "app", "origin": "page", "sessionId": "57c8ff1c-a4ea-4ea0-b5a5-99474e00691b",
#         "stationId": "94e9a8c5-fcdf-41dc-9e6a-0613025024d5", "sendAnalytics": 'true'}
#
# response = requests.post('https://ontopo.co.il/api/availability/searchAvailability', headers=headers, json=data)
# res = response.json()
# print(res)

"""How does it fetch all the available times of a single restaurant: 
We have something call options. it present all of the options times of the restaurant, 
options is a list of dictionary and each dictionary present some hour, inside that dictionary we have something call method.
 when the method is 'disabled' that mean the option  (the hour we choose) is taken and not available, 
 but when method is 'seat' that mean the option is available and we can order that option."""
#
# for i in range(0,len(res['areas'])):
#     print(res['areas'][i]['id'])
#     print(res['areas'][i]['options'])

# if res['areas'][i]['method']=='seat':

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
    'referer': 'https://ontopo.co.il/results/?region=%D7%AA%D7%9C%20%D7%90%D7%91%D7%99%D7%91&size=2&date=20211113&time=2300&market=4342499',
    'accept-language': 'he',
    'cookie': '_gcl_au=1.1.1683183408.1636663583; _ga=GA1.3.2084581254.1636663583; _gid=GA1.3.641795585.1636663583; _fbp=fb.2.1636663584969.2003306758; _gat_UA-113921616-2=1; auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsiYW5vbnltb3VzIl0sIngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6ImFub255bW91cyJ9LCJpYXQiOjE2MzY3NDkyOTcsImV4cCI6MTYzNjc1MDE5N30.ucQDR5nFiDRTTRz_dNw4w5t6aPYT_jxFXoVwYuglNTI; auth_refresh_token=69c2bf73-2bcd-4c2c-90cb-3dd7a6237e3c; auth_token_expired=2021-11-12T20%3A44%3A57Z',
}

data = {"directory": "culinary.pages.il", "locale": "he",
        "filter": {"location": {"lat": 32.0650841, "lon": 34.7708837}, "distance": 5, "component": "reservation"},
        "size": 400, "search_after": [], "market": "XzW03HZwb"}

response = requests.post('https://ontopo.co.il/api/results/searchVenues', headers=headers, json=data)
res = response.json()
print(res)
# for i in range(0,len(res['venues'])):
#     print(res['venues'][i])
