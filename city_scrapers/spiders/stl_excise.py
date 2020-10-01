import re
from datetime import datetime

import scrapy
from city_scrapers_core.constants import COMMITTEE
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class StlExciseSpider(CityScrapersSpider):
    name = "stl_excise"
    agency = "St. Louis Excise Division"
    timezone = "America/Chicago"
    custom_settings = {"ROBOTSTXT_OBEY": False}
    start_urls = [
        (
            "https://www.stlouis-mo.gov/events/"
            "past-meetings.cfm?span=-30&department=370"
        ),
        "https://www.stlouis-mo.gov/events/all-public-meetings.cfm?span=30",
    ]

    def parse(self, response):
        for url in self._get_event_urls(response):
            yield scrapy.Request(url=url, callback=self._parse_event)

    def _get_event_urls(self, response):
        event_urls = response.css("ul.list-group h4 a::attr(href)").getall()
        event_sponsors = response.css("ul.list-group li span.small::text").getall()
        urls = []
        for url, sponsor in zip(event_urls, event_sponsors):
            if "excise division" in sponsor.lower():
                urls.append(response.urljoin(url))
        return urls

    def _parse_event(self, response):
        """
        `parse` should always `yield` Meeting items.
        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        meeting = Meeting(
            title="Liquor License Application Hearings",
            description="",
            classification=COMMITTEE,
            start=self._parse_start(response),
            end=self._parse_end(response),
            all_day=False,
            location=self._parse_location(response),
            links=[],
            source=response.url,
        )
        meeting["status"] = self._get_status(meeting)
        meeting["id"] = self._get_id(meeting)
        yield meeting

    def _parse_description(self, response):
        """Parse or generate meeting description."""
        return ""

    def _parse_start(self, response):
        """Parse start datetime as a naive datetime object."""
        date = response.css("div.page-title-row p.page-summary::text").get()
        pattern = r"(?P<day>\d{2}/\d{2}/\d{2}), (?P<time>(\d{1,2}:\d{2}) (PM|AM))"
        pattern += r" - (\d{1,2}:\d{2}) (PM|AM)"
        rm = re.search(pattern, date)

        if rm is not None:
            day = rm.group("day")
            time = rm.group("time")
            dt = day + " " + time
            start = datetime.strptime(dt.strip(), "%m/%d/%y %H:%M %p")
            return start
        else:
            return None

    def _parse_end(self, response):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        date = response.css("div.page-title-row p.page-summary::text").get()
        pattern = r"(?P<day>\d{2}/\d{2}/\d{2}), (\d{1,2}:\d{2}) (PM|AM)"
        pattern += r" - (?P<time>(\d{1,2}:\d{2}) (PM|AM))"
        rm = re.search(pattern, date)

        if rm is not None:
            day = rm.group("day")
            time = rm.group("time")
            dt = day + " " + time
            end = datetime.strptime(dt.strip(), "%m/%d/%y %H:%M %p")
            return end
        else:
            return None

    def _parse_location(self, response):
        """Parse or generate location."""
        location = response.css("div.col-md-4 div.content-block p *::text").getall()

        temp = []
        for item in location:
            item = item.replace("\n", "").replace("\t", "")
            if item != "":
                temp.append(item)
        location = temp
        i, location_index, sponsor_index = 0, 0, 0
        while i < len(location):
            if "location" in location[i].lower():
                location_index = i
            if "sponsor" in location[i].lower():
                sponsor_index = i
                break
            i += 1

        if (
            location_index + 1 < len(location)
            and sponsor_index < len(location)
            and location_index != sponsor_index
        ):
            name = location[location_index + 1]
            address = []
            for j in range(location_index + 2, sponsor_index):
                temp = location[j].replace(", ", ",").replace(",", ", ")
                temp = temp.replace("\t", "")
                address.append(temp)
            address = (
                " ".join(address).replace("Directions to this address", "").strip()
            )
        else:
            name = ""
            address = ""

        description = response.css("div#EventDisplayBlock p::text").getall()
        description = "".join(description)

        if description is not None:
            if "teleconference" in description.lower():
                name = "Teleconference"
                address = ""

        return {
            "address": address,
            "name": name,
        }
