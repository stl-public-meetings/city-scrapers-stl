from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import COMMITTEE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.cc_arts import CcArtsSpider

test_response = file_response(
    join(dirname(__file__), "files", "cc_arts.html"),
    url="https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5053",
)
spider = CcArtsSpider()

freezer = freeze_time("2020-07-02")
freezer.start()
item = spider._parse_event(test_response)
freezer.stop()


def test_title():
    assert item["title"] == "Arts Committee"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2019, 1, 23, 6, 0)


def test_end():
    assert item["end"] == datetime(2019, 1, 23, 8, 0)


def test_id():
    assert item["id"] == "cc_arts/201901230600/x/arts_committee"


def test_status():
    assert item["status"] == "passed"


def test_location():
    assert item["location"] == {
        "name": "PW Administrative Conference Room",
        "address": "300 N New Ballas Road Creve Coeur, MO  63141",
    }


def test_source():
    assert (
        item["source"]
        == "https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5053"
    )


def test_links():
    assert item["links"] == [
        {
            "href": (
                "https://crevecoeurcitymo.iqm2.com/Citizens/"
                "FileOpen.aspx?Type=14&ID=1944&Inline=True"
            ),
            "title": "Agenda",
        },
        {
            "href": (
                "https://crevecoeurcitymo.iqm2.com/Citizens/"
                "FileOpen.aspx?Type=12&ID=4683&Inline=True"
            ),
            "title": "Minutes",
        },
    ]


def test_classification():
    assert item["classification"] == COMMITTEE


def test_all_day():
    assert item["all_day"] is False
