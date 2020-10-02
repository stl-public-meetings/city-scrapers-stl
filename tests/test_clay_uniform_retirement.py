from datetime import datetime
from os.path import dirname, join

from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.clay_uniform_retirement import ClayUniformRetirementSpider

test_response = file_response(
    join(dirname(__file__), "files", "clay_uniform_retirement.html"),
    url=(
        "https://www.claytonmo.gov/government/\
        boards-and-commissions/uniformed-employees-retirement-board"
    ),
)
spider = ClayUniformRetirementSpider()

freezer = freeze_time("2020-10-02")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]
print(parsed_items)
freezer.stop()

"""
def test_tests():
    print("Please write some tests for this spider or at least disable this one.")
    assert False
"""

"""
Uncomment below
"""


def test_title():
    type(parsed_items)
    assert parsed_items[0]["title"] == "Uniformed Employees Retirement Board"


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2020, 10, 8, 8, 0)


# def test_end():
#    assert parsed_items[0]["end"] == datetime(2020, 10, 8, 10, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert (
        parsed_items[0]["id"]
        == "clay_uniform_retirement/202010080800/x/uniformed_employees_retirement_board"
    )


def test_status():
    assert parsed_items[0]["status"] == "tentative"


def test_location():
    assert parsed_items[0]["location"] == {"name": "", "address": "Missouri"}


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://www.claytonmo.gov/government/\
        boards-and-commissions/uniformed-employees-retirement-board"
    )


# def test_links():
#     assert parsed_items[0]["links"] == [{
#       "href": "EXPECTED HREF",
#       "title": "EXPECTED TITLE"
#     }]


def test_classification():
    assert parsed_items[0]["classification"] == "BOARD"


# @pytest.mark.parametrize("item", parsed_items)
# def test_all_day(item):
#     assert item["all_day"] is False
