from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.cc_personnel_appeals import CcPersonnelAppealsSpider

test_response = file_response(
    join(dirname(__file__), "files", "cc_personnel_appeals.html"),
    url="https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5745",
)
spider = CcPersonnelAppealsSpider()

freezer = freeze_time("2020-07-02")
freezer.start()
item = spider._parse_event(test_response)
freezer.stop()


def test_title():
    assert item["title"] == "Personnel Appeals Board"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2020, 6, 22, 5, 0)


def test_end():
    assert item["end"] == datetime(2020, 6, 22, 7, 0)


def test_id():
    assert item["id"] == "cc_personnel_appeals/202006220500/x/personnel_appeals_board"


def test_status():
    assert item["status"] == "passed"


def test_location():
    assert item["location"] == {
        "name": "Online Meeting",
        "address": "",
    }


def test_source():
    assert (
        item["source"]
        == "https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5745"
    )


def test_links():
    assert item["links"] == [
        {
            "href": (
                "https://crevecoeurcitymo.iqm2.com/Citizens/"
                "FileOpen.aspx?Type=14&ID=2167&Inline=True"
            ),
            "title": "Agenda",
        },
        {
            "href": (
                "https://crevecoeurcitymo.iqm2.com/Citizens/"
                "FileOpen.aspx?Type=12&ID=5245&Inline=True"
            ),
            "title": "Minutes",
        },
    ]


def test_classification():
    assert item["classification"] == BOARD


def test_all_day():
    assert item["all_day"] is False
