from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import COMMISSION
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.stl_tax_financing import StlTaxFinancingSpider

test_response = file_response(
    join(dirname(__file__), "files", "stl_tax_financing.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=25283",
)
test_detail_response = file_response(
    join(dirname(__file__), "files", "stl_tax_financing_detail.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=25283",
)
spider = StlTaxFinancingSpider()

freezer = freeze_time("2020-07-22")
freezer.start()

spider._parse_links(test_detail_response)
item = spider._parse_event(test_response)

freezer.stop()


def test_title():
    assert item["title"] == "Tax Increment Financing Commission"


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2020, 4, 15, 8, 0)


def test_end():
    assert item["end"] == datetime(2020, 4, 15, 10, 0)


def test_id():
    assert (
        item["id"]
        == "stl_tax_financing/202004150800/x/tax_increment_financing_commission"
    )


def test_status():
    assert item["status"] == "passed"


def test_location():
    assert item["location"] == {
        "name": "Call-In or Video Conference",
        "address": "",
    }


def test_source():
    assert (
        item["source"]
        == "https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=25283"
    )


def test_links():
    assert item["links"] == [
        {
            "href": (
                "https://www.stlouis-mo.gov/government/departments/sldc/boards/"
                "documents/upload/TIF-Board-Packet-2.pdf"
            ),
            "title": "Agenda",
        }
    ]


def test_classification():
    assert item["classification"] == COMMISSION


def test_all_day():
    assert item["all_day"] is False
