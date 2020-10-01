from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.stl_zoning import StlZoningSpider

test_response = file_response(
    join(dirname(__file__), "files", "stl_zoning.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=24580",
)

test_detail_response = file_response(
    join(dirname(__file__), "files", "stl_zoning_detail.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=24580",
)

spider = StlZoningSpider()

freezer = freeze_time("2020-07-12")
freezer.start()
spider._parse_links(test_detail_response)
item = spider._parse_event(test_response)

freezer.stop()


def test_title():
    assert item["title"] == "Board of Adjustment"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2020, 7, 8, 1, 30)


def test_end():
    assert item["end"] == datetime(2020, 7, 8, 5, 0)


def test_id():
    assert item["id"] == "stl_zoning/202007080130/x/board_of_adjustment"


def test_status():
    assert item["status"] == "passed"


def test_location():
    assert item["location"] == {
        "name": "City Hall",
        "address": "1200 Market Street, Room 208 St. Louis, MO 63103",
    }


def test_source():
    assert (
        item["source"]
        == "https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=24580"
    )


def test_links():
    assert item["links"] == [
        {
            "href": (
                "https://www.stlouis-mo.gov/government/departments/public-safety/"
                "building/zoning/documents/upload/"
                "PN07-08-20-Agenda-for-Virtual-Meeting.pdf"
            ),
            "title": "Agenda",
        },
    ]


def test_classification():
    assert item["classification"] == BOARD


def test_all_day():
    assert item["all_day"] is False
