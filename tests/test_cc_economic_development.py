from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import COMMITTEE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.cc_economic_development import CcEconomicDevelopmentSpider

test_response = file_response(
    join(dirname(__file__), "files", "cc_economic_development.html"),
    url="https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5002",
)
spider = CcEconomicDevelopmentSpider()

freezer = freeze_time("2020-07-04")
freezer.start()

item = spider._parse_event(test_response)

freezer.stop()


def test_title():
    assert item["title"] == "Economic Development Committee"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2019, 1, 15, 8, 0)


def test_end():
    assert item["end"] == datetime(2019, 1, 15, 10, 0)


def test_time_notes():
    assert item["time_notes"] == ""


def test_id():
    assert (
        item["id"]
        == "cc_economic_development/201901150800/x/economic_development_committee"
    )


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
        == "https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5002"
    )


def test_links():
    assert item["links"] == [
        {
            "title": "Minutes",
            "href": (
                "https://crevecoeurcitymo.iqm2.com/Citizens/"
                "FileOpen.aspx?Type=12&ID=4681&Inline=True"
            ),
        },
    ]


def test_classification():
    assert item["classification"] == COMMITTEE


def test_all_day():
    assert item["all_day"] is False
