from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import COMMISSION
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.cc_planning import CcPlanningSpider

test_response = file_response(
    join(dirname(__file__), "files", "cc_planning.html"),
    url="https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5059",
)
spider = CcPlanningSpider()

freezer = freeze_time("2020-07-04")
freezer.start()

item = spider._parse_event(test_response)

freezer.stop()


def test_title():
    assert item["title"] == "Planning and Zoning Commission"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2019, 1, 7, 6, 30)


def test_end():
    assert item["end"] == datetime(2019, 1, 7, 8, 30)


def test_time_notes():
    assert item["time_notes"] == ""


def test_id():
    assert item["id"] == "cc_planning/201901070630/x/planning_and_zoning_commission"


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
        == "https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5059"
    )


def test_links():
    assert item["links"] == [
        {
            "title": "Agenda",
            "href": (
                "https://crevecoeurcitymo.iqm2.com/Citizens/"
                "FileOpen.aspx?Type=14&ID=1938&Inline=True"
            ),
        },
        {
            "title": "Minutes",
            "href": (
                "https://crevecoeurcitymo.iqm2.com/Citizens/"
                "FileView.aspx?Type=12&ID=4676"
            ),
        },
    ]


def test_classification():
    assert item["classification"] == COMMISSION


def test_all_day():
    assert item["all_day"] is False
