import unittest
import holidays


class TestACDCHoliday(unittest.TestCase):

    def test_to_json(self):
        holiday = holidays.Holiday("Christmas", "25/12", 2016)

        expected = {
            "holiday": {
                "name": "Christmas",
                "date": "25/12/2016",
                "year": 2016,
                "city": "",
                "country": ""
            }
        }
        self.assertEqual(expected, holiday.to_json())

    def test_to_json_start_time(self):
        holiday = holidays.Holiday("Christmas", "25/12", 2016, start_time='00:00:00', end_time='12:00:00')

        self.assertEqual("00:00:00", holiday.to_json()["start_time"])
        self.assertEqual("12:00:00", holiday.to_json()["end_time"])
