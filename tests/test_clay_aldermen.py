from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.clay_aldermen import ClayAldermenSpider

test_response = file_response(
    join(dirname(__file__), "files", "clay_aldermen.html"),
    url="https://www.claytonmo.gov/Home/Components/Calendar/Event/4732",
)

test_detail_response = file_response(
    join(dirname(__file__), "files", "clay_aldermen_detail.html"),
    url="https://www.claytonmo.gov/Home/Components/Calendar/Event/4732",
)

spider = ClayAldermenSpider()

freezer = freeze_time("2020-07-28")
freezer.start()

spider._parse_links(test_detail_response)
parsed_items = [item for item in spider._parse_event(test_response)]

freezer.stop()


def test_title():
    assert parsed_items[0]["title"] == "Board of Aldermen"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2020, 6, 23, 7, 0)


def test_end():
    assert parsed_items[0]["end"] == datetime(2020, 6, 23, 7, 59)


def test_id():
    assert parsed_items[0]["id"] == "clay_aldermen/202006230700/x/board_of_aldermen"


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "City Hall - Council Chamber",
        "address": "10 N. Bemiston Clayton, Missouri 63105",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://www.claytonmo.gov/Home/Components/Calendar/Event/4732"
    )


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "href": (
                "https://www.claytonmo.gov/Home/Components/MeetingsManager/"
                "MeetingAgenda/ShowPrimaryDocument/?agendaID=2245&isPub=True&"
                "includeTrash=False"
            ),
            "title": "Agenda",
        },
        {
            "href": (
                "https://www.claytonmo.gov/Home/Components/MeetingsManager/"
                "MeetingMinutes/ShowPrimaryDocument/?minutesID=3060&isPub=True&"
                "includeTrash=False"
            ),
            "title": "Minutes",
        },
    ]


def test_classification():
    assert parsed_items[0]["classification"] == BOARD


# @pytest.mark.parametrize("item", parsed_items)
def test_all_day():
    # assert item["all_day"] is False
    assert parsed_items[0]["all_day"] is False
