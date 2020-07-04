from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.cc_venable_park import CcVenableParkSpider

test_response = file_response(
    join(dirname(__file__), "files", "cc_venable_park.html"),
    url="https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5697",
)
spider = CcVenableParkSpider()

freezer = freeze_time("2020-07-04")
freezer.start()

item = spider._parse_event(test_response)

freezer.stop()


def test_title():
    assert item["title"] == "Dr. H. Venable Memorial Park Task Force"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2020, 4, 15, 7, 0)


def test_end():
    assert item["end"] == datetime(2020, 4, 15, 9, 0)


def test_time_notes():
    assert item["time_notes"] == ""


def test_id():
    assert (
        item["id"]
        == "cc_venable_park/202004150700/x/dr_h_venable_memorial_park_task_force"
    )


def test_status():
    assert item["status"] == "passed"


def test_location():
    assert item["location"] == {"name": "Online Meeting", "address": ""}


def test_source():
    assert (
        item["source"]
        == "https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5697"
    )


def test_links():
    assert item["links"] == [
        {
            "href": (
                "https://crevecoeurcitymo.iqm2.com/Citizens/"
                "FileOpen.aspx?Type=14&ID=2133&Inline=True"
            ),
            "title": "Agenda",
        },
        {
            "href": (
                "https://crevecoeurcitymo.iqm2.com/Citizens/"
                "FileOpen.aspx?Type=12&ID=5215&Inline=True"
            ),
            "title": "Minutes",
        },
    ]


def test_classification():
    assert item["classification"] == NOT_CLASSIFIED


def test_all_day():
    assert item["all_day"] is False
