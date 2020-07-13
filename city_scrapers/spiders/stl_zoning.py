import re
from collections import defaultdict
from datetime import datetime

import scrapy
from city_scrapers_core.constants import BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class StlZoningSpider(CityScrapersSpider):
    name = "stl_zoning"
    agency = "St. Louis Zoning Section"
    timezone = "America/Chicago"
    custom_settings = {"ROBOTSTXT_OBEY": False}
    start_urls = [
        (
            "https://www.stlouis-mo.gov/government/departments/public-safety/"
            "building/zoning/documents/agendas-board-adjustment.cfm"
        ),
        (
            "https://www.stlouis-mo.gov/government/departments/public-safety/"
            "building/zoning/documents/agendas-conditional-use.cfm"
        )
    ]

    def __init__(self, *args, **kwargs):
        self.agenda_map_adjustment = defaultdict(list)
        self.agenda_map_conditional = defaultdict(list)
        super().__init__(*args, **kwargs)

    def parse(self, response):
        self._parse_meeting_materials(response)
        print('\n')
        print('\n')
        yield None

    def _parse_meeting_materials(self, response):
        for url in self._get_agenda_urls(response):
            url = response.urljoin(url)
            print(url)
            resp = scrapy.Request(url=url, method="GET", callback=self._parse_links, dont_filter=True)
            print("hi")
        # yield None
    
    def _get_agenda_urls(self, response):
        urls = response.css("td.CS_PgIndex_Item a::attr(href)").getall()[:3]
        urls += response.css("td.CS_PgIndex_Item_Alternate a::attr(href)").getall()[:3]
        return urls
        
    def _parse_event(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.css(".meetings"):
            meeting = Meeting(
                title=self._parse_title(item),
                description=self._parse_description(item),
                classification=BOARD,
                start=self._parse_start(item),
                end=self._parse_end(item),
                all_day=self._parse_all_day(item),
                time_notes=self._parse_time_notes(item),
                location=self._parse_location(item),
                links=self._parse_links(item),
                source=self._parse_source(response),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_title(self, response):
        """Parse or generate meeting title."""
        return ""

    def _parse_description(self, response):
        """Parse or generate meeting description."""
        return ""

    def _parse_start(self, response):
        """Parse start datetime as a naive datetime object."""
        return None

    def _parse_end(self, response):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, response):
        """Parse any additional notes on the timing of the meeting"""
        return ""

    def _parse_all_day(self, response):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, response):
        """Parse or generate location."""
        return {
            "address": "",
            "name": "",
        }

    def _parse_links(self, response):
        """Parse or generate links."""
        # agency = response.css("div.cs_control h1::text").get()
        # links = response.css("li a::attr(href)").getall()
        # descriptions = response.css("li a::text").getall()
        # print(agency)
        # print(len(links))
        # print(len(descriptions))
        print("links")



    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
