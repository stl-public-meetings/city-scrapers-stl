from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.stl_industrial_development import (
    StlIndustrialDevelopmentSpider,
)

test_response = file_response(
    join(dirname(__file__), "files", "stl_industrial_development.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=24624",
)

test_detail_response = file_response(
    join(dirname(__file__), "files", "stl_industrial_development_detail.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=24624",
)
spider = StlIndustrialDevelopmentSpider()

freezer = freeze_time("2020-07-21")
freezer.start()

spider._parse_links(test_detail_response)
item = spider._parse_event(test_response)

freezer.stop()


def test_title():
    assert item["title"] == "Industrial Development Authority"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2020, 1, 9, 1, 30)


def test_end():
    assert item["end"] == datetime(2020, 1, 9, 2, 30)


def test_id():
    assert (
        item["id"]
        == "stl_industrial_development/202001090130/x/industrial_development_authority"
    )


def test_status():
    assert item["status"] == "passed"


def test_location():
    assert item["location"] == {
        "name": "SLDC Board Room, 2nd Floor",
        "address": "1520 Market Street, Suite 2000 St. Louis, MO 63103",
    }


def test_source():
    assert (
        item["source"]
        == "https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=24624"
    )


def test_links():
    assert item["links"] == [
        {
            "href": (
                "https://www.stlouis-mo.gov/government/departments/sldc/boards/"
                "documents/upload/January-9-2020-IDA-Regular-Board-Meeting-Agenda.pdf"
            ),
            "title": "Agenda",
        },
        {
            "href": (
                "https://www.stlouis-mo.gov/government/departments/sldc/boards/"
                "documents/upload/January-9-2020-IDA-Regular-Board-Meeting-Minutes.pdf"
            ),
            "title": "Minutes",
        },
    ]


def test_classification():
    assert item["classification"] == BOARD


def test_all_day():
    assert item["all_day"] is False
