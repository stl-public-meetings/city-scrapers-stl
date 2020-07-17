from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.stl_preservation import StlPreservationSpider

test_response = file_response(
    join(dirname(__file__), "files", "stl_preservation.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=26421",
)

test_detail_response = file_response(
    join(dirname(__file__), "files", "stl_preservation_detail.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=26421",
)
spider = StlPreservationSpider()

freezer = freeze_time("2020-07-15")
freezer.start()

spider._parse_links(test_detail_response)
item = spider._parse_event(test_response)

freezer.stop()


def test_title():
    assert item["title"] == "Preservation Board"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2020, 6, 29, 4, 0)


def test_end():
    assert item["end"] == datetime(2020, 6, 29, 7, 0)


def test_id():
    assert item["id"] == "stl_preservation/202006290400/x/preservation_board"


def test_status():
    assert item["status"] == "passed"


def test_location():
    assert item["location"] == {
        "name": "Abrams Building",
        "address": "1520 MARKET ST. #2000 St. Louis, MO 63103",
    }


def test_source():
    assert (
        item["source"]
        == "https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=26421"
    )


def test_links():
    assert item["links"] == [
        {
            "href": (
                "https://www.stlouis-mo.gov/government/departments/planning/"
                "cultural-resources/documents/upload/"
                "FINAL-AGENDA-WITH-ZOOM-PAGE-6-29-20-3.pdf"
            ),
            "title": "Agenda",
        },
        {
            "href": (
                "https://www.stlouis-mo.gov/government/departments/planning/"
                "cultural-resources/documents/upload/JUNE-2020-POWERPOINT.pptx"
            ),
            "title": "Presentation",
        },
    ]


def test_classification():
    assert item["classification"] == BOARD


def test_all_day():
    assert item["all_day"] is False
