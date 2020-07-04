from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import COMMITTEE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.cc_parks_preservation import CcParksPreservationSpider

test_response = file_response(
    join(dirname(__file__), "files", "cc_parks_preservation.html"),
    url="https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5681",
)
spider = CcParksPreservationSpider()

freezer = freeze_time("2020-07-02")
freezer.start()
item = spider._parse_event(test_response)
freezer.stop()


def test_title():
    assert item["title"] == "Parks and Historic Preservation Committee"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2020, 2, 12, 5, 0)


def test_end():
    assert item["end"] == datetime(2020, 2, 12, 7, 0)


def test_id():
    id = (
        "cc_parks_preservation/202002120500/x/parks_and_historic_preservation_committee"
    )
    assert item["id"] == id


def test_status():
    assert item["status"] == "passed"


def test_location():
    assert item["location"] == {
        "name": "Dielmann West",
        "address": "11400 Olde Cabin Road Creve Coeur, MO  63141",
    }


def test_source():
    assert (
        item["source"]
        == "https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5681"
    )


def test_links():
    assert item["links"] == [
        {
            "href": (
                "https://crevecoeurcitymo.iqm2.com/Citizens/"
                "FileOpen.aspx?Type=12&ID=5217&Inline=True"
            ),
            "title": "Minutes",
        },
    ]


def test_classification():
    assert item["classification"] == COMMITTEE


def test_all_day():
    assert item["all_day"] is False
