from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import COMMITTEE
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.stl_excise import StlExciseSpider

test_response = file_response(
    join(dirname(__file__), "files", "stl_excise.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=26703",
)
spider = StlExciseSpider()

freezer = freeze_time("2020-08-07")
freezer.start()

parsed_items = [item for item in spider._parse_event(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "Liquor License Application Hearings"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2020, 8, 6, 9, 0)


def test_end():
    assert parsed_items[0]["end"] == datetime(2020, 8, 6, 10, 30)


def test_id():
    assert parsed_items[0]["id"] == (
        "stl_excise/202008060900/x/liquor_license_application_hearings"
    )


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "EXCISE DIVISION",
        "address": "1200 MARKET ST, CITY HALL ROOM 418 St. Louis, MO 63101",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=26703"
    )


def test_links():
    assert parsed_items[0]["links"] == []


def test_classification():
    assert parsed_items[0]["classification"] == COMMITTEE


def test_all_day():
    assert parsed_items[0]["all_day"] is False
