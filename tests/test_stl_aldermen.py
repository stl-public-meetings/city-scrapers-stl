from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.stl_aldermen import StlAldermenSpider

test_response = file_response(
    join(dirname(__file__), "files", "stl_aldermen.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=26489",
)

test_detail_response = file_response(
    join(dirname(__file__), "files", "stl_aldermen_detail.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=26489",
)


spider = StlAldermenSpider()

freezer = freeze_time("2020-07-09")
freezer.start()
spider._parse_links(test_detail_response)
item = spider._parse_event(test_response)
freezer.stop()


def test_title():
    assert item["title"] == "Full Board of Aldermen"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2020, 7, 8, 1, 0)


def test_end():
    assert item["end"] == datetime(2020, 7, 8, 3, 0)


def test_id():
    assert item["id"] == "stl_aldermen/202007080100/x/full_board_of_aldermen"


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
        == "https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=26489"
    )


def test_links():
    assert item["links"] == [
        {
            "href": (
                "https://www.stlouis-mo.gov/internal-apps/"
                "legislative/upload/agenda/7-8-20 AGENDA 14 2.pdf"
            ),
            "title": "Agenda",
        },
        {
            "href": (
                "https://www.stlouis-mo.gov/internal-apps/"
                "legislative/upload/minute/BOA Minutes 7-8-20 Updated2.pdf"
            ),
            "title": "Minutes",
        },
    ]


def test_classification():
    assert item["classification"] == BOARD


def test_all_day():
    assert item["all_day"] is False
