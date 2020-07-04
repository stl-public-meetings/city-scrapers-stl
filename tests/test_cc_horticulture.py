from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import COMMITTEE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.cc_horticulture import CcHorticultureSpider

test_response = file_response(
    join(dirname(__file__), "files", "cc_horticulture.html"),
    url="https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5088",
)
spider = CcHorticultureSpider()

freezer = freeze_time("2020-07-04")
freezer.start()

item = spider._parse_event(test_response)

freezer.stop()


def test_title():
    assert item["title"] == "Horticulture, Ecology and Beautification Committee"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2019, 1, 9, 4, 0)


def test_end():
    assert item["end"] == datetime(2019, 1, 9, 6, 0)


def test_time_notes():
    assert item["time_notes"] == ""


def test_id():
    assert item["id"] == (
        "cc_horticulture/201901090400/x/"
        "horticulture_ecology_and_beautification_committee"
    )


def test_status():
    assert item["status"] == "passed"


def test_location():
    assert item["location"] == {
        "name": "Dielmann West",
        "address": ("11400 Olde Cabin Road Creve Coeur, MO  63141"),
    }


def test_source():
    assert (
        item["source"]
        == "https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5088"
    )


def test_links():
    assert item["links"] == [
        {
            "title": "Agenda",
            "href": (
                "https://crevecoeurcitymo.iqm2.com/Citizens/"
                "FileOpen.aspx?Type=14&ID=1939&Inline=True"
            ),
        },
        {
            "title": "Minutes",
            "href": (
                "https://crevecoeurcitymo.iqm2.com/Citizens/"
                "FileOpen.aspx?Type=12&ID=4677&Inline=True"
            ),
        },
    ]


def test_classification():
    assert item["classification"] == COMMITTEE


def test_all_day():
    assert item["all_day"] is False
