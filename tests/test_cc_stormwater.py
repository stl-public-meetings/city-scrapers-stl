from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import COMMITTEE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.cc_stormwater import CcStormwaterSpider

test_response = file_response(
    join(dirname(__file__), "files", "cc_stormwater.html"),
    url="https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5675",
)
spider = CcStormwaterSpider()

freezer = freeze_time("2020-07-04")
freezer.start()

item = spider._parse_event(test_response)

freezer.stop()


def test_title():
    assert item["title"] == "Stormwater Committee"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2020, 4, 15, 4, 30)


def test_end():
    assert item["end"] == datetime(2020, 4, 15, 6, 30)


def test_time_notes():
    assert item["time_notes"] == ""


def test_id():
    assert item["id"] == "cc_stormwater/202004150430/x/stormwater_committee"


def test_status():
    assert item["status"] == "passed"


def test_location():
    assert item["location"] == {"name": "Online Meeting", "address": ""}


def test_source():
    assert (
        item["source"]
        == "https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5675"
    )


def test_links():
    assert item["links"] == [
        {
            "href": (
                "https://crevecoeurcitymo.iqm2.com/Citizens/"
                "FileOpen.aspx?Type=14&ID=2131&Inline=True"
            ),
            "title": "Agenda",
        },
        {
            "href": (
                "https://crevecoeurcitymo.iqm2.com/Citizens/"
                "FileOpen.aspx?Type=12&ID=5233&Inline=True"
            ),
            "title": "Minutes",
        },
    ]


def test_classification():
    assert item["classification"] == COMMITTEE


def test_all_day():
    assert item["all_day"] is False
