import requests

ACDC_URL = "http://localhost.acdc.avenuecode.io:3000"


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


def gather_national_holidays(year):
    url = "http://dadosbr.github.io/feriados/nacionais.json"

    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()

        for value in data:
            parsed_holiday = translate_national_holiday(value, 2016)
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
    print r.text
    if r.status_code == 200:
        print r.text
        return True
    return False



#gather_national_holidays(2016)


