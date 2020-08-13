from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.stl_forest_park_advisory import StlForestParkAdvisory

test_response = file_response(
    join(dirname(__file__), "files", "stl_forest_park_advisory.html"),
    url="https://www.stlouis-mo.gov/events/eventdetails.cfm?Event_ID=18292"
)

test_agenda_response = file_response(
    join(dirname(__file__), "files", "stl_forest_park_advisory_details.html"),
    url="https://sites.google.com/a/stlouis-mo.gov/forest-park-master-plan/home"
)

test_minute_response = file_response(
    join(dirname(__file__), "files", "stl_forest_park_advisory_details.html"),
    url="https://sites.google.com/a/stlouis-mo.gov/forest-park-master-plan/home"
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

def test_description():
    description = "The Forest Park Advisory Board was established in 1996 by Ordinance 63769 to provide ongoing citizen input into the implementation of the Forest Park Master Plan. FPAB's primary role is to review Park improvement projects and monitor compliance with the Master Plan for all major park projects, both privately-funded and City-funded projects. The Board is part of a larger ongoing public review process and, as such, reviews each proposed project at three steps during the project's design.The Board makes recommendations to the Director of Parks, Recreation, and Forestry.Join Zoom Meeting:Meeting ID: 974 4608 2041Password: 088982One tap mobile: USDial by your location USMeeting ID: 974 4608 2041Find your local number: Please review the posted ZOOM CHEAT SHEET prior to the meeting. Please try to join the meeting 10-15 minutes early to work out any kinks in your connection, displays, sound, etc.Agenda and presentation materials are available from the Forest Park Master Plan Website link below.Jun 19, 2018 3:58 PMJul 14, 2020 1:47 PM"
    assert item["description"] == description

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
            "href": "https://sites.google.com/a/stlouis-mo.gov/forest-park-master-plan/home/FPAB%20Agenda%202020-07-16.pdf?attredirects=0&d=1"
        }
    ]