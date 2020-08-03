from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.stl_civilian import StlCivilianSpider

test_response = file_response(
    join(dirname(__file__), "files", "stl_civilian.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=26420",
)

test_detail_response = file_response(
    join(dirname(__file__), "files", "stl_civilian_detail.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=26420",
)

spider = StlCivilianSpider()

freezer = freeze_time("2020-08-02")
freezer.start()

spider._parse_links(test_detail_response)
item = spider._parse_event(test_response)
freezer.stop()


def test_title():
    assert item["title"] == "Civilian Oversight Board"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2020, 6, 15, 5, 0)


def test_end():
    assert item["end"] == datetime(2020, 6, 15, 6, 0)


def test_id():
    assert item["id"] == "stl_civilian/202006150500/x/civilian_oversight_board"


def test_status():
    assert item["status"] == "passed"


def test_location():
    assert item["location"] == {
        "name": "Teleconference",
        "address": "",
    }


def test_source():
    assert (
        item["source"]
        == "https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=26420"
    )


def test_links():
    assert item["links"] == [
        {
            "href": (
                "https://www.stlouis-mo.gov/government/departments/public-safety/"
                "civilian-oversight-board/documents/upload/June-15-2020-Open-"
                "Agenda-final.pdf"
            ),
            "title": "Agenda",
        },
    ]


def test_classification():
    assert item["classification"] == BOARD


def test_all_day():
    assert item["all_day"] is False
