# coding=utf-8
import requests

ACDC_URL = "http://localhost.acdc.avenuecode.io:3000"
american_regions = {
    "California": "San Francisco",
    "Ohio": "Lorain",
    "New York": "New York",
    "Florida": "Jacksonville",
    "Pennsylvania": "Pittsburgh"
}


AMERICAN_HOLIDAYS_DB = {}
AMERICAN_HOLIDAYS = {}


class Holiday(object):
    """
    ACDC Representation of a holiday
    """
    def __init__(self, name, date, year, city="", country="", start_time=None, end_time=None):
        self.name = name
        self.date = "{0}/{1}".format(date, year)
        self.year = year
        self.city = city
        self.country = country
        self.start_time = start_time
        self.end_time = end_time

    def to_json(self):
        json = {
            "holiday": {
                "name": self.name,
                "date": self.date,
                "city": self.city,
                "country": self.country
            }
        }
        if self.start_time:
            json["start_time"] = self.start_time
        if self.end_time:
            json["end_time"] = self.end_time

        return json


def seed_american_db(year):
    global AMERICAN_HOLIDAYS_DB, AMERICAN_HOLIDAYS
    url = "http://kayaposoft.com/enrico/json/v1.0/?" \
          "action=getPublicHolidaysForYear&year={}&country=usa&region=".format(year)
    r = requests.get(url)
    if r.status_code == 200:
        AMERICAN_HOLIDAYS_DB = r.json()

    for holiday in AMERICAN_HOLIDAYS_DB:
        date = "{}/{}".format(holiday['date']['day'], holiday['date']['month'])
        holiday_name = holiday['englishName']
        AMERICAN_HOLIDAYS[holiday_name] = date


def translate_national_holiday(data, year):
    date = data["date"]
    if str(year) in data['variableDates']:
        date = "{}/{}".format(data['variableDates'][str(year)], year)
    holiday = Holiday(
        name=data["title"],
        date=date,
        year=year,
        country="Brazil"
    )
    return holiday.to_json()


def translate_state_holiday(data, year, state):
    date = data["date"]
    if str(year) in data['variableDates']:
        date = "{}/{}".format(data['variableDates'][str(year)], year)

    city = ""
    if state == 'MG':
        city = "Belo Horizonte"
    elif state == 'SP':
        city = u"São Paulo"

    holiday = Holiday(
        name=data["title"],
        date=date,
        year=year,
        city=city
    )
    return holiday.to_json()


def gather_state_brazilian_holidays(state, year):
    url = "http://dadosbr.github.io/feriados/estaduais/{}.json".format(state)

    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()

        for value in data:
            parsed_holiday = translate_state_holiday(value, year, state)
            if not insert_holiday(parsed_holiday):
                print("Could not create holiday {}".format(parsed_holiday))


def translate_american_holidays(data, year, region=None):

    date = "{}/{}".format(data["date"]["day"], data["date"]["month"])
    holiday = Holiday(
        name=data["englishName"],
        date=date,
        year=year,
        country="USA"
    )
    if region is not None:
        holiday.city = region
        holiday.country = ""

    return holiday.to_json()


def holiday_exists(name, date):
    holiday_date = "{}/{}".format(date['day'], date['month'])
    global AMERICAN_HOLIDAYS

    if name in AMERICAN_HOLIDAYS:
        return True

    dates = [value for value in AMERICAN_HOLIDAYS.itervalues()]
    if holiday_date in dates:
        return True

    return False


def is_optional(data):
    try:
        return data['note'] == 'optional'
    except KeyError:
        return False


def gather_local_american_holidays(local, year):
    url = "http://kayaposoft.com/enrico/json/v1.0/?" \
          "action=getPublicHolidaysForYear&year={}&country=usa&region={}".format(year, local)
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()

        for value in data:
            if not is_optional(value):
                if not holiday_exists(value['englishName'], value['date']):
                    parsed_holiday = translate_american_holidays(value, year, american_regions[local])
                    if not insert_holiday(parsed_holiday):
                        print("Could not create holiday {}".format(parsed_holiday))
            else:
                print value


def gather_american_holidays(year):
    url = "http://kayaposoft.com/enrico/json/v1.0/?" \
          "action=getPublicHolidaysForYear&year={}&country=usa&region=".format(year)
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()

        for value in data:
            parsed_holiday = translate_american_holidays(value, year)
            if not insert_holiday(parsed_holiday):
                print("Could not create holiday {}".format(parsed_holiday))


def gather_national_holidays(year):
    url = "http://dadosbr.github.io/feriados/nacionais.json"

    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()

        for value in data:
            parsed_holiday = translate_national_holiday(value, year)
            if not insert_holiday(parsed_holiday):
                print("Could not create holiday {}".format(parsed_holiday))


def insert_holiday(holiday):
    headers = {'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfaWQiOiI1N2VhZjY1YTdjMjA4MzQ0N2ViOTFkM'
                                 'jkiLCJkaXNwbGF5TmFtZSI6IkFDIE11bGUiLCJuYW1lIjp7ImZhbWlseU5hbWUiOiIiLCJnaXZlbk5'
                                 'hbWUiOiJBQ01VTEUifSwiZW1haWwiOiJhYy1tdWxlQGF2ZW51ZWNvZGUuY29tIiwiZ29vZ2xlSWQiOi'
                                 'I5OTk5OTk5OTk5OTk5OTk5OTk5OTkiLCJpbWFnZSI6IiIsImdlbmRlciI6IiIsImF1dGhvcml6YXRpb'
                                 '24iOiJkODMxMDFjZmExZDlhNDJjNzgxMTZjMThlMDU0Mjg1NDQzZTRhOTZkMDI3ODhiYTgyY2JiNmNhNm'
                                 'FhNTc4ODlmZGY2MTZjMDk5YjkwNTg1ZjFlODkzNTY1NTRjOWMxM2U2NjE0M2QwODRkMmUwMzY0Yzk4ZDcy'
                                 'NWY5NTkwZmQzMyIsInNzb1RlYW0iOmZhbHNlLCJyb2xlIjoiZW1wbG95ZWUiLCJhY2Nlc3NCbG9ja2VkIj'
                                 'pmYWxzZSwiY3JlYXRlZEF0IjoiMjAxNi0xMC0yOFQxMjozMzo1NC4xMzRaIiwiaWF0IjoxNDc3NjU4MDM0'
                                 'fQ.kmv2jdi_AJ198wBtkaIrWRExPi4r_9yLev6zzfb-2io',
               'Content-type': 'application/json'}
    url = "{}/api/holidays".format(ACDC_URL)
    r = requests.post(url, json=holiday, headers=headers)
    if r.status_code == 200:
        print r.text
        return True
    return False


gather_american_holidays(2016)
gather_national_holidays(2016)
gather_state_brazilian_holidays('MG', 2016)
gather_state_brazilian_holidays('SP', 2016)

seed_american_db(2016)
for region in american_regions.iterkeys():
    gather_local_american_holidays(region, 2016)