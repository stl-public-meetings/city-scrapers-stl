from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.cc_building_code import CcBuildingCodeSpider

test_response = file_response(
    join(dirname(__file__), "files", "cc_building_code.html"),
    url="https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5698",
)
spider = CcBuildingCodeSpider()

freezer = freeze_time("2020-07-02")
freezer.start()
item = spider._parse_event(test_response)
freezer.stop()


def test_title():
    assert item["title"] == "Building Code Board of Appeals"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2020, 3, 19, 5, 30)


def test_end():
    assert item["end"] == datetime(2020, 3, 19, 7, 30)


def test_id():
    assert (
        item["id"] == "cc_building_code/202003190530/x/building_code_board_of_appeals"
    )


def test_status():
    assert item["status"] == "passed"


def test_location():
    assert item["location"] == {
        "name": "Phone Conference",
        "address": "",
    }


def test_source():
    assert (
        item["source"]
        == "https://crevecoeurcitymo.iqm2.com/Citizens/Detail_Meeting.aspx?ID=5698"
    )


def test_links():
    assert item["links"] == [
        {
            "href": (
                "https://crevecoeurcitymo.iqm2.com/Citizens/"
                "FileOpen.aspx?Type=14&ID=2136&Inline=True"
            ),
            "title": "Agenda",
        },
        {
            "href": (
                "https://crevecoeurcitymo.iqm2.com/Citizens/"
                "FileOpen.aspx?Type=12&ID=5210&Inline=True"
            ),
            "title": "Minutes",
        },
    ]


def test_classification():
    assert item["classification"] == BOARD


def test_all_day():
    assert item["all_day"] is False
