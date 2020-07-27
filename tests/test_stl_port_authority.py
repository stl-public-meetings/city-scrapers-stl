from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.stl_port_authority import StlPortAuthority

test_response = file_response(
    join(dirname(__file__), "files", "stl_port_authority.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=20519",
)

test_detail_response = file_response(
    join(dirname(__file__), "files", "stl_port_authority_detail.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=20519",
)
spider = StlPortAuthority()

freezer = freeze_time("2020-07-25")
freezer.start()

spider._parse_links(test_detail_response)
item = spider._parse_event(test_response)

freezer.stop()


def test_title():
    assert item["title"] == "Port Authority Commission"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2020, 7, 16, 9, 30)


def test_end():
    assert item["end"] == datetime(2020, 7, 16, 10, 30)


def test_id():
    assert item["id"] == ("stl_port_authority/202007160930/x/port_authority_commission")


def test_status():
    assert item["status"] == "passed"


def test_location():
    assert item["location"] == {
        "name": "Zoom",
        "address": (""),
    }


def test_source():
    assert (
        item["source"]
        == "https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=20519"
    )


def test_links():
    assert item["links"] == [
        {
            "title": "Agenda",
            "href": (
                "https://www.stlouis-mo.gov/government/departments/sldc/boards"
                "/documents/upload/July-16-2020-Port-Authority-Regular"
                "-Board-Meeting-Agenda.docx"
            ),
        },
    ]


def test_classification():
    assert item["classification"] == BOARD


def test_all_day():
    assert item["all_day"] is False
