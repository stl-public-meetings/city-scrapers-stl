from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import COMMITTEE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.cc_audit import CcAuditSpider

test_response = file_response(
    join(dirname(__file__), "files", "cc_audit.html"),
    url="https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5179",
)
spider = CcAuditSpider()

freezer = freeze_time("2020-07-03")
freezer.start()

item = spider._parse_event(test_response)

freezer.stop()


def test_title():
    assert item["title"] == "Audit  Committee"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2019, 8, 8, 9, 30)


def test_end():
    assert item["end"] == datetime(2019, 8, 8, 11, 30)


def test_time_notes():
    assert item["time_notes"] == ""


def test_id():
    assert item["id"] == "cc_audit/201908080930/x/audit_committee"


def test_status():
    assert item["status"] == "passed"


def test_location():
    assert item["location"] == {
        "name": "Administrative Conference Room",
        "address": "300 N New Ballas Road Creve Coeur, MO  63141",
    }


def test_source():
    assert (
        item["source"]
        == "https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5179"
    )


def test_links():
    assert item["links"] == [
        {
            "href": "https://crevecoeurcitymo.iqm2.com/Citizens/FileOpen"
            ".aspx?Type=14&ID=2023&Inline=True",
            "title": "Agenda",
        },
        {
            "title": "Minutes",
            "href": "https://crevecoeurcitymo.iqm2.com/Citizens/FileOpen"
            ".aspx?Type=12&ID=4779&Inline=True",
        },
    ]


def test_classification():
    assert item["classification"] == COMMITTEE


def test_all_day():
    assert item["all_day"] is False
