from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.stl_redevelopment import StlRedevelopmentSpider

test_response = file_response(
    join(dirname(__file__), "files", "stl_redevelopment.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=24656",
)
test_detail_response = file_response(
    join(dirname(__file__), "files", "stl_redevelopment_detail.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=24656",
)
spider = StlRedevelopmentSpider()

freezer = freeze_time("2020-07-18")
freezer.start()

spider._parse_links(test_detail_response)
item = spider._parse_event(test_response)

freezer.stop()


def test_title():
    assert item["title"] == "Land Clearance for Redevelopment Authority"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2020, 6, 23, 3, 0)


def test_end():
    assert item["end"] == datetime(2020, 6, 23, 5, 0)


def test_id():
    assert (
        item["id"]
        == "stl_redevelopment/202006230300/x/land_clearance_for_redevelopment_authority"
    )


def test_status():
    assert item["status"] == "passed"


def test_location():
    assert item["location"] == {
        "name": "2nd Floor Board Room",
        "address": "1520 Market St. St. Louis, MO 63103",
    }


def test_source():
    assert (
        item["source"]
        == "https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=24656"
    )


def test_links():
    assert item["links"] == [
        {
            "href": (
                "https://www.stlouis-mo.gov/government/departments/sldc/boards/"
                "documents/upload/June-23-2020-LCRA-Regular-Meeting-Agenda.pdf"
            ),
            "title": "Agenda",
        }
    ]


def test_classification():
    assert item["classification"] == BOARD


def test_all_day():
    assert item["all_day"] is False
