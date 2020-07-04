from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import COMMITTEE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.cc_finance import CcFinanceSpider

test_response = file_response(
    join(dirname(__file__), "files", "cc_finance.html"),
    url="https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5011",
)
spider = CcFinanceSpider()

freezer = freeze_time("2020-07-04")
freezer.start()

item = spider._parse_event(test_response)

freezer.stop()


def test_title():
    assert item["title"] == "Finance Committee"


def test_description():
    assert item["description"] == "Meeting Cancelled"


def test_start():
    assert item["start"] == datetime(2019, 2, 12, 5, 30)


def test_end():
    assert item["end"] == datetime(2019, 2, 12, 7, 30)


def test_time_notes():
    assert item["time_notes"] == ""


def test_id():
    assert item["id"] == "cc_finance/201902120530/x/finance_committee"


def test_status():
    assert item["status"] == "cancelled"


def test_location():
    assert item["location"] == {
        "name": "Administrative Conference Room",
        "address": ("300 N New Ballas Road Creve Coeur, MO  63141"),
    }


def test_source():
    assert (
        item["source"]
        == "https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5011"
    )


def test_links():
    assert item["links"] == [
        {
            "title": "Agenda",
            "href": (
                "https://crevecoeurcitymo.iqm2.com/Citizens/"
                "FileOpen.aspx?Type=14&ID=1958&Inline=True"
            ),
        },
    ]


def test_classification():
    assert item["classification"] == COMMITTEE


def test_all_day():
    assert item["all_day"] is False
