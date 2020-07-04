from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.cc_adjustment import CcAdjustmentSpider

test_response = file_response(
    join(dirname(__file__), "files", "cc_adjustment.html"),
    url="https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5040",
)
spider = CcAdjustmentSpider()

freezer = freeze_time("2020-07-04")
freezer.start()

item = spider._parse_event(test_response)

freezer.stop()


def test_title():
    assert item["title"] == "Board of Adjustment"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2019, 3, 21, 4, 0)


def test_end():
    assert item["end"] == datetime(2019, 3, 21, 6, 0)


def test_time_notes():
    assert item["time_notes"] == ""


def test_id():
    assert item["id"] == "cc_adjustment/201903210400/x/board_of_adjustment"


def test_status():
    assert item["status"] == "passed"


def test_location():
    assert item["location"] == {
        "name": "City Council Chamber",
        "address": (
            "300 North New Ballas Rd City of Creve Coeur Government Center "
            "Creve Coeur, MO  63141"
        ),
    }


def test_source():
    assert (
        item["source"]
        == "https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5040"
    )


def test_links():
    assert item["links"] == [
        {
            "title": "Agenda",
            "href": (
                "https://crevecoeurcitymo.iqm2.com/Citizens/"
                "FileOpen.aspx?Type=14&ID=1973&Inline=True"
            ),
        },
        {
            "title": "Minutes",
            "href": (
                "https://crevecoeurcitymo.iqm2.com/Citizens/"
                "FileOpen.aspx?Type=12&ID=4713&Inline=True"
            ),
        },
    ]


def test_classification():
    assert item["classification"] == BOARD


def test_all_day():
    assert item["all_day"] is False
