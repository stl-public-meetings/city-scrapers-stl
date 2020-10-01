from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import COMMISSION
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.stl_land_reutilization import StlLandReutilizationSpider

test_response = file_response(
    join(dirname(__file__), "files", "stl_land_reutilization.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=23202",
)

test_detail_response = file_response(
    join(dirname(__file__), "files", "stl_land_reutilization_detail.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=23202",
)
spider = StlLandReutilizationSpider()

freezer = freeze_time("2020-07-24")
freezer.start()

spider._parse_links(test_detail_response)
item = spider._parse_event(test_response)

freezer.stop()


def test_title():
    assert item["title"] == "Land Reutilization Commission"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2020, 6, 24, 8, 30)


def test_end():
    assert item["end"] == datetime(2020, 6, 24, 9, 30)


def test_id():
    assert (
        item["id"]
        == "stl_land_reutilization/202006240830/x/land_reutilization_commission"
    )


def test_status():
    assert item["status"] == "passed"


def test_location():
    assert item["location"] == {
        "name": "Webinar",
        "address": "",
    }


def test_source():
    assert (
        item["source"]
        == "https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=23202"
    )


def test_links():
    assert item["links"] == [
        {
            "href": (
                "https://www.stlouis-mo.gov/government/departments/sldc/"
                "boards/documents/upload/6-24-20-Agenda-Posting-4.pdf"
            ),
            "title": "Agenda",
        }
    ]


def test_classification():
    assert item["classification"] == COMMISSION


def test_all_day():
    assert item["all_day"] is False
