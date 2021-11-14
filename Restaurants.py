from rich import print
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
    'referer': 'https://ontopo.co.il/results/?region=%D7%AA%D7%9C%20%D7%90%D7%91%D7%99%D7%91&size=2&date=20211111&time=2000&market=4342499',
    'accept-language': 'he,en-US;q=0.9,en;q=0.8',
    'cookie': '_ga=GA1.3.705025712.1624537679; _gcl_au=1.1.1553806650.1636522977; _gid=GA1.3.1953460068.1636522980; auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsiYW5vbnltb3VzIl0sIngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6ImFub255bW91cyJ9LCJpYXQiOjE2MzY2MjMxMDQsImV4cCI6MTYzNjYyNDAwNH0.5jaUJY46V9Q8F7gQsEY7FQqe_Un5RzFV9GTjVT9Stno; auth_refresh_token=12475110-19f9-45cc-b29e-0f2a69bc5e45; auth_token_expired=2021-11-11T09%3A41%3A44Z; _gat_UA-113921616-2=1',
}

data = {"directory": "culinary.pages.il", "locale": "he",
        "filter": {"location": {"lat": 32.0650841, "lon": 34.7708837}, "distance": 5, "component": "reservation"},
        "size": 227, "search_after": "", "market": "XzW03HZwb"}

response = requests.post('https://ontopo.co.il/api/results/searchVenues', headers=headers, json=data)
res = response.json()
for i in range(0,len(res['venues'])):
    print(res['venues'][i]['pageId'])

