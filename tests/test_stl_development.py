from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.stl_development import StlDevelopmentSpider

test_response = file_response(
    join(dirname(__file__), "files", "stl_development.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=21838",
)

test_detail_response = file_response(
    join(dirname(__file__), "files", "stl_development_detail.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=21838",
)
spider = StlDevelopmentSpider()

freezer = freeze_time("2020-07-23")
freezer.start()

spider._parse_links(test_detail_response)
item = spider._parse_event(test_response)

freezer.stop()


def test_title():
    assert item["title"] == "St. Louis Local Development Company Board"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2020, 7, 9, 3, 0)


def test_end():
    assert item["end"] == datetime(2020, 7, 9, 5, 0)


def test_id():
    assert (
        item["id"]
        == "stl_development/202007090300/x/st_louis_local_development_company_board"
    )


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
        == "https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=21838"
    )


def test_links():
    assert item["links"] == [
        {
            "href": (
                "https://www.stlouis-mo.gov/government/departments/sldc/boards/"
                "documents/upload/luly-9-2020-StL-Local-Dev-Company-Regular-"
                "Board-Meeting-Packet.pdf"
            ),
            "title": "Agenda",
        }
    ]


def test_classification():
    assert item["classification"] == BOARD


def test_all_day():
    assert item["all_day"] is False
