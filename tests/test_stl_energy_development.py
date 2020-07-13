from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.stl_energy_development import StlEnergyDevelopment

test_response = file_response(
    join(dirname(__file__), "files", "stl_energy_development.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=24838",
)
spider = StlEnergyDevelopment()

freezer = freeze_time("2020-07-04")
freezer.start()

item = spider._parse_event(test_response)

freezer.stop()


def test_title():
    title = "Clean Energy Development Board Quarterly Board Meeting via Zoom"
    assert item["title"] == title


def test_description():
    assert item["description"] == ""


def test_start():
    assert item["start"] == datetime(2020, 5, 7, 3, 0)


def test_end():
    assert item["end"] == datetime(2020, 5, 7, 4, 30)


def test_time_notes():
    assert item["time_notes"] == ""


def test_id():
    assert item["id"] == (
        "stl_energy_development/202005070300/x/clean_energy"
        "_development_board_quarterly_board_meeting_via_zoom"
    )


def test_status():
    assert item["status"] == "passed"


def test_location():
    assert item["location"] == {
        "name": "Clean Energy Development Board",
        "address": (""),
    }


def test_source():
    assert (
        item["source"]
        == "https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=24838"
    )


def test_links():
    assert item["links"] == [
        {
            "title": "Agenda",
            "href": (
                "https://www.stlouis-mo.gov/government/departments"
                "/sldc/boards/documents/may-7-2020-cedb-quarterly-board"
                "-meeting-via-zoom-meeting-materials.cfm"
            ),
        },
    ]


def test_classification():
    assert item["classification"] == BOARD


def test_all_day():
    assert item["all_day"] is False
