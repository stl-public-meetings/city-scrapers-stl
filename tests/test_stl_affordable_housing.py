from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import COMMISSION
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.stl_affordable_housing import StlAffordableHousingSpider

test_response = file_response(
    join(dirname(__file__), "files", "stl_affordable_housing.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=26726",
)

test_detail_response = file_response(
    join(dirname(__file__), "files", "stl_affordable_housing_detail.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=26726",
)

spider = StlAffordableHousingSpider()

freezer = freeze_time("2020-09-24")
freezer.start()
spider._parse_links(test_detail_response)
item = spider._parse_event(test_response)

freezer.stop()


def test_title():
    assert item["title"] == "Affordable Housing Commission"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2020, 9, 11, 11, 30)


def test_end():
    assert item["end"] == datetime(2020, 9, 11, 12, 30)


def test_id():
    assert item["id"] == (
        "stl_affordable_housing/202009111130/x/affordable_housing_commission"
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
        == "https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=26726"
    )


def test_links():
    assert item["links"] == [
        {
            "href": (
                "https://www.stlouis-mo.gov/government/departments/affordable-"
                "housing/documents/upload/091120-agenda.pdf"
            ),
            "title": "Agenda",
        },
    ]


def test_classification():
    assert item["classification"] == COMMISSION


def test_all_day():
    assert item["all_day"] is False
