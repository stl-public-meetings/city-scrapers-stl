from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import COMMITTEE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.stl_criminal_justice import StlCriminalJusticeSpider

test_response = file_response(
    join(dirname(__file__), "files", "stl_criminal_justice.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=24911",
)

test_detail_response = file_response(
    join(dirname(__file__), "files", "stl_criminal_justice_detail.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=24911",
)

spider = StlCriminalJusticeSpider()

freezer = freeze_time("2020-08-06")
freezer.start()

spider._parse_links(test_detail_response)
parsed_items = [item for item in spider._parse_event(test_response)]
freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "Information Sharing Governance Committee"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2020, 8, 5, 2, 0)


def test_end():
    assert parsed_items[0]["end"] == datetime(2020, 8, 5, 4, 0)


def test_id():
    assert parsed_items[0]["id"] == (
        "stl_criminal_justice/202008050200/x/"
        "information_sharing_governance_committee"
    )


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Videoconference",
        "address": "",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=24911"
    )


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "href": (
                "https://www.stlouis-mo.gov/government/departments/mayor/"
                "initiatives/cjcc/documents/upload/August-5-2020-Agenda-Info-"
                "Sharing-Goverance-Committee.pdf"
            ),
            "title": "Agenda",
        },
    ]


def test_classification():
    assert parsed_items[0]["classification"] == COMMITTEE


def test_all_day():
    assert parsed_items[0]["all_day"] is False
