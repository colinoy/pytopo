import requests
from rich import print
import datetime as dt
import json
import re

ENTRIES_CACHE = {}


def get_restaurant_schedule_raw(restaurant_id="junowine"):
    headers = {
        'sec-ch-ua': '"Opera GX";v="81", " Not;A Brand";v="99", "Chromium";v="95"',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://ontopo.co.il/',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 OPR/81.0.4196.61',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = (
        ('directory', 'culinary.pages.il'),
        ('page_id', restaurant_id),
        ('locale', 'he'),
    )

    response = requests.get(
        'https://ontopo.co.il/api/content', headers=headers, params=params)
    return response.json()


def parse_string_into_list_of_ints(string):
    '''
    Parses a string of numbers and a range of numbers into a list of ints
    Example input: "1,4-6,8"
    Example output: [1,4,5,6,8]
    '''
    if string == "":
        return []

    if ',' in string:
        all_parts = string.split(",")
    else:
        all_parts = [string]

    result = []
    for part in all_parts:
        if '-' in part:
            start, end = part.split("-")
            for i in range(int(start), int(end)+1):
                result.append(i)
        else:
            result.append(int(part))
    return result


def get_restaurant_schedule_parsed(restaurant_id="junowine"):
    '''
    Parses the raw json from the restaurant schedule api
    '''
    raw_result = get_restaurant_schedule_raw(restaurant_id)
    shifts = raw_result['content']['shifts']['shifts']
    # print(shifts)

    step = shifts['time']['step']

    # Result dict setup
    entries = dict()
    entries['weekdays'] = dict()
    entries['dates'] = dict()

    for opening in shifts['opening']:
        min_start_time_str = opening['default']
        min_start_time = dt.datetime.strptime(
            min_start_time_str, "%H%M").time()
        max_end_time_str = opening['last']
        max_end_time = dt.datetime.strptime(max_end_time_str, "%H%M").time()

        # Entries are in the format:
        # 'hours': {'a': {'time': '1100-1430'}, 'b': {'tag': 'walkin', 'time': '1430-1700'}, 'c': {'time': '1800-2200'}}
        hour_entries = dict()
        for hour_entry in opening['hours'].values():
            if not 'time' in hour_entry:
                continue
            hour_entry_start_time_str = hour_entry['time'].split("-")[0]
            hour_entry_start_time = dt.datetime.strptime(
                hour_entry_start_time_str, "%H%M").time()
            hour_entry_end_time_str = hour_entry['time'].split("-")[1]
            hour_entry_end_time = dt.datetime.strptime(
                hour_entry_end_time_str, "%H%M").time()

            # Limit the range of hours to the min and max times
            hour_entry_start_time = min(min_start_time, hour_entry_start_time)
            hour_entry_end_time = min(max_end_time, hour_entry_end_time)

            now = hour_entry_start_time
            while now <= hour_entry_end_time:
                if now not in hour_entries:
                    hour_entries[now] = hour_entry['tag'] if 'tag' in hour_entry else ""
                now = (dt.datetime.combine(dt.date(1, 1, 1), now) +
                       dt.timedelta(minutes=step)).time()

        # Add the hour entries to the appropriate days of the week or custom dates

        if '__criteria' in opening:
            if 'weekday' in opening['__criteria']:
                weekdays = opening['__criteria']['weekday']
                weekdays = parse_string_into_list_of_ints(weekdays)
                for day in weekdays:
                    entries['weekdays'][day] = hour_entries
            if 'date' in opening['__criteria']:
                date = opening['__criteria']['date']
                date = dt.datetime.strptime(date, '%Y%m%d')
                entries['dates'][date] = hour_entries

    return entries


def get_restaurant_full_schedule(restaurant_id):
    '''
    Returns the full schedule for a restaurant
    Uses a chache to avoid making multiple requests
    '''
    global ENTRIES_CACHE
    if restaurant_id not in ENTRIES_CACHE:
        ENTRIES_CACHE[restaurant_id] = get_restaurant_schedule_parsed(
            restaurant_id)
    return ENTRIES_CACHE[restaurant_id]


def get_restaurant_schedule_for_day(restaurant_id, day):
    '''
    Returns the schedule for a restaurant for a specific day
    '''
    entries = get_restaurant_full_schedule(restaurant_id)
    if day in entries['dates']:
        return entries['dates'][day]

    # Convert weekday int into jewish week standard
    weekday = day.isoweekday() % 7

    if weekday in entries['weekdays']:
        return entries['weekdays'][weekday]
    return {}


if __name__ == "__main__":
    import requests
    # print(get_restaurant_schedule_for_day("shishko", dt.datetime.strptime("20220118", "%Y%m%d")))

