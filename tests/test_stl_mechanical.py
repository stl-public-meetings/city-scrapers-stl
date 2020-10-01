from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.stl_mechanical import StlMechanicalSpider

test_response = file_response(
    join(dirname(__file__), "files", "stl_mechanical.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=25158",
)
spider = StlMechanicalSpider()

freezer = freeze_time("2020-07-27")
freezer.start()

parsed_items = [item for item in spider._parse_event(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "Stationary Engineer Board"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2020, 7, 2, 9, 30)


def test_end():
    assert parsed_items[0]["end"] == datetime(2020, 7, 2, 12, 00)


def test_id():
    assert (
        parsed_items[0]["id"]
        == "stl_mechanical/202007020930/x/stationary_engineer_board"
    )


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "City Hall, room 426 conference room",
        "address": "1200 Market St. St. Louis, MO 63103",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=25158"
    )


def test_links():
    assert parsed_items[0]["links"] == []


def test_classification():
    assert parsed_items[0]["classification"] == BOARD
