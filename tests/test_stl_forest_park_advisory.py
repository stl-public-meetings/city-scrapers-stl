from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.stl_forest_park_advisory import StlForestParkAdvisory

test_response = file_response(
    join(dirname(__file__), "files", "stl_forest_park_advisory.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=18292",
)

test_agenda_response = file_response(
    join(dirname(__file__), "files", "stl_forest_park_advisory_details.html"),
    url="https://sites.google.com/a/stlouis-mo.gov/forest-park-master-plan/home",
)

test_minute_response = file_response(
    join(dirname(__file__), "files", "stl_forest_park_advisory_details.html"),
    url="https://sites.google.com/a/stlouis-mo.gov/forest-park-master-plan/home",
)

spider = StlForestParkAdvisory()

freezer = freeze_time("2020-07-16")
freezer.start()

spider._get_agenda_urls(test_agenda_response)
spider._get_minute_urls(test_minute_response)
item = spider._parse_event(test_response)

freezer.stop()


def test_title():
    title = "Forest Park Advisory Board via Zoom"
    assert item["title"] == title


def test_start():
    assert item["start"] == datetime(2020, 7, 16, 4, 30)


def test_end():
    assert item["end"] == datetime(2020, 7, 16, 5, 30)


def test_location():
    assert item["location"] == {
        "name": "Zoom",
        "address": (""),
    }


def test_links():
    assert item["links"] == [
        {
            "title": "FPAB Agenda 2020-07-16.pdf",
            "href": (
                "https://sites.google.com/a/stlouis-mo.gov/"
                "forest-park-master-plan/home/FPAB%20Agenda"
                "%202020-07-16.pdf?attredirects=0&d=1"
            ),
        }
    ]
