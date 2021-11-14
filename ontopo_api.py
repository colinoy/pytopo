import requests


# from rich import print

def main():
    headers = {
        'authority': 'ontopo.co.il',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json;charset=UTF-8',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'origin': 'https://ontopo.co.il',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://ontopo.co.il/arestauranttlv/',
        'accept-language': 'he,en-US;q=0.9,en;q=0.8',
        'cookie': '_ga=GA1.3.705025712.1624537679; _gcl_au=1.1.1553806650.1636522977; auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsiYW5vbnltb3VzIl0sIngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6ImFub255bW91cyIsIngtaGFzdXJhLXVzZXItaWQiOiIwMWU3YWYxMi0xMjRjLTQ5YzYtYTg5Ni1mM2Y5MjU4MDU1MzIifSwiaWF0IjoxNjM2NTIyOTc2LCJleHAiOjE2MzY1MjM4NzZ9.b7QzocZUaSaKBoa1Yrp10UuJ6MrrybSHq7zN1Ie-42g; auth_refresh_token=e375b61a-f9e2-4e05-9bcd-53fc45e6151c; auth_token_expired=2021-11-10T05%3A52%3A56Z; _gid=GA1.3.1953460068.1636522980; _gat_UA-113921616-2=1',
    }
    my_size = '5'
    resturant_id = "aresturant"
    data = {"page_id": resturant_id, "locale": "he", "criteria": {"size": my_size, "date": "20211210", "time": "1830"},
            "app": "web", "origin": "marketplace", "sessionId": "b760d78b-9e27-44d1-b4af-34fa0e2af28f",
            "stationId": "fd0f0464-1637-4baf-9aea-1821ecaa8d54", "sendAnalytics": "true"}

    response = requests.post('https://ontopo.co.il/api/availability/searchAvailability', headers=headers, json=data)
    print(response.content)


if __name__ == '__main__':
    main()
