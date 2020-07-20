from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.stl_enterprise_zone import StlEnterpriseZoneSpider

test_response = file_response(
    join(dirname(__file__), "files", "stl_enterprise_zone.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=24666",
)

test_detail_response = file_response(
    join(dirname(__file__), "files", "stl_enterprise_zone_detail.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=24666",
)

spider = StlEnterpriseZoneSpider()

freezer = freeze_time("2020-07-20")
freezer.start()

spider._parse_links(test_detail_response)
item = spider._parse_event(test_response)

freezer.stop()


def test_title():
    assert item["title"] == "CANCELLED-Enhanced Enterprise Zone Board"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2020, 4, 21, 3, 0)


def test_end():
    assert item["end"] == datetime(2020, 4, 21, 5, 0)


def test_id():
    assert (
        item["id"]
        == "stl_enterprise_zone/202004210300/x/enhanced_enterprise_zone_board"
    )


def test_status():
    assert item["status"] == "cancelled"


def test_location():
    assert item["location"] == {
        "name": "Zoom",
        "address": "",
    }


def test_source():
    assert (
        item["source"]
        == "https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=24666"
    )


def test_links():
    assert item["links"] == [
        {
            "href": (
                "https://www.stlouis-mo.gov/government/departments/sldc/boards/"
                "documents/upload/EEZ-Packet.pdf"
            ),
            "title": "Agenda",
        }
    ]


def test_classification():
    assert item["classification"] == BOARD


def test_all_day():
    assert item["all_day"] is False
