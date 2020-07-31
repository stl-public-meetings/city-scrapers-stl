from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.stl_development_corp import StlDevelopmentCorpSpider

test_response = file_response(
    join(dirname(__file__), "files", "stl_development_corp.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=23435",
)

test_detail_response = file_response(
    join(dirname(__file__), "files", "stl_development_corp_detail.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=23435",
)

spider = StlDevelopmentCorpSpider()

freezer = freeze_time("2020-07-30")
freezer.start()

spider._parse_links(test_detail_response)
item = spider._parse_event(test_response)
freezer.stop()


def test_title():
    assert item["title"] == "St. Louis Development Corporation"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2020, 7, 16, 8, 0)


def test_end():
    assert item["end"] == datetime(2020, 7, 16, 9, 0)


def test_id():
    assert item["id"] == "stl_development_corp/202007160800/x/st_louis_development_corporation"


def test_status():
    assert item["status"] == "passed"


def test_location():
    assert item["location"] == {
        "name": "Zoom",
        "address": "",
    }


def test_source():
    assert (
        item["source"]
        == "https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=23435"
    )


def test_links():
    assert item["links"] == [
        {
            "href": (
                "https://www.stlouis-mo.gov/government/departments/sldc/boards/"
                "documents/upload/July-16-2020-SLDC-Board-Meeting-via-Zoom-Agenda-"
                "Packet.pdf"
            ),
            "title": "Agenda",
        },
    ]


def test_classification():
    assert item["classification"] == BOARD


def test_all_day():
    assert item["all_day"] is False