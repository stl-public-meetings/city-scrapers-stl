from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import COMMITTEE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.cc_police_safety import CcPoliceSafetySpider

test_response = file_response(
    join(dirname(__file__), "files", "cc_police_safety.html"),
    url="https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5147",
)
spider = CcPoliceSafetySpider()

freezer = freeze_time("2020-07-02")
freezer.start()
item = spider._parse_event(test_response)
freezer.stop()


def test_title():
    assert item["title"] == "Police and Safety Committee"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2019, 3, 12, 5, 30)


def test_end():
    assert item["end"] == datetime(2019, 3, 12, 7, 30)


def test_id():
    assert item["id"] == "cc_police_safety/201903120530/x/police_and_safety_committee"


def test_status():
    assert item["status"] == "passed"


def test_location():
    assert item["location"] == {
        "name": "City Council Chamber",
        "address": "300 North New Ballas Rd City of Creve Coeur"
        " Government Center Creve Coeur, MO  63141",
    }


def test_source():
    assert (
        item["source"]
        == "https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5147"
    )


def test_links():
    assert item["links"] == [
        {
            "href": (
                "https://crevecoeurcitymo.iqm2.com/Citizens/"
                "FileOpen.aspx?Type=14&ID=1970&Inline=True"
            ),
            "title": "Agenda",
        },
    ]


def test_classification():
    assert item["classification"] == COMMITTEE


def test_all_day():
    assert item["all_day"] is False
