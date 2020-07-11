from datetime import datetime, timedelta
import re

import scrapy
from city_scrapers_core.constants import COMMITTEE, BOARD, NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.relativedelta import relativedelta


class StlAldermenSpider(CityScrapersSpider):
    name = "stl_aldermen"
    agency = "St. Louis Board of Aldermen"
    timezone = "America/Chicago"
    custom_settings = {"ROBOTSTXT_OBEY": False}
    start_urls = [
        "https://www.stlouis-mo.gov/events/past-meetings.cfm?span=-60&department=332",
        # "https://www.stlouis-mo.gov/events/all-public-meetings.cfm?span=60"
    ]

    # def start_requests(self):
    #     url = "https://www.stlouis-mo.gov/events/all-public-meetings.cfm"
    #     yield scrapy.Request(url=url, method="GET", callback=self._parse_test)
    
    def parse(self, response):
        for url in self._get_event_urls(response):
            yield scrapy.Request(url, callback=self._parse_event, dont_filter=True)

    def _get_event_urls(self, response):
        event_urls = response.css("ul.list-group h4 a::attr(href)").getall()
        event_sponsors = response.css("ul.list-group li span.small::text").getall()
        urls = []
        for url, sponsor in zip(event_urls, event_sponsors):
            # print('\n')
            # print("a")
            # print(sponsor)
            # print("b")
            # print(response.urljoin(url))
            # print('\n')
            if "aldermen" in sponsor.lower() or "aldermanic" in sponsor.lower():
                urls.append(response.urljoin(url))
        return urls

    def _parse_event(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        meeting = Meeting(
            title=self._parse_title(response),
            description=self._parse_description(response),
            classification=self._parse_classification(response),
            start=self._parse_start(response),
            end=self._parse_end(response),
            all_day=self._parse_all_day(response),
            location=self._parse_location(response),
            links=self._parse_links(response),
            source=response.url,
        )

        meeting["status"] = self._get_status(meeting)
        meeting["id"] = self._get_id(meeting)
        yield meeting
        # return None

    def _parse_title(self, response):
        """Parse or generate meeting title."""
        title = response.css("div.page-title-row h1::text").get()
        title = title.replace("Meeting", "").replace("Metting", "")
        # title = title.replace("(", "").replace(")","").replace("-", "- ")
        title = title.replace("-", "- ")
        # title = title.replace("Canceled", "Cancelled")
        title = title.replace("(Canceled)", "Cancelled")
        return title.replace("  ", " ")

    def _parse_description(self, response):
        """Parse or generate meeting description."""
        description = response.css("div#EventDisplayBlock div.col-md-8 h4 strong::text").getall()
        i = 0
        while i < len(description) - 1:
            if "following:" in description[i]:
                return description[i+1].replace("\xa0","")
            elif "will" in description[i]:
                return description[i].replace("\xa0","")
            else:
                i += 1
        else:
            return ""

    def _parse_classification(self, response):
        """Parse or generate classification from allowed options."""
        title = response.css("div.page-title-row h1::text").get()
        if "committee" in title.lower():
            return COMMITTEE
        elif "board" in title.lower():
            return BOARD
        else:
            return NOT_CLASSIFIED

    def _parse_start(self, response):
        """Parse start datetime as a naive datetime object."""
        date = response.css("div.page-title-row p.page-summary::text").get()
        pattern = "(?P<day>\d{2}/\d{2}/\d{2}), (?P<time>(\d{1,2}:\d{2}) (PM|AM)) - (\d{1,2}:\d{2}) (PM|AM)"
        rm = re.search(pattern, date)
        # print('\n')
        # print(date)
        
        if rm is not None:
            day = rm.group("day")
            time = rm.group("time")
            dt = day + " " + time
            start = datetime.strptime(dt.strip(), "%m/%d/%y %H:%M %p")
            # print(dt)
            # print('\n')
            return start
        else:
            return None

    def _parse_end(self, response):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        date = response.css("div.page-title-row p.page-summary::text").get()
        pattern = "(?P<day>\d{2}/\d{2}/\d{2}), (\d{1,2}:\d{2}) (PM|AM) - (?P<time>(\d{1,2}:\d{2}) (PM|AM))"
        rm = re.search(pattern, date)
        # print('\n')
        # print(date)
        
        if rm is not None:
            day = rm.group("day")
            time = rm.group("time")
            dt = day + " " + time
            end = datetime.strptime(dt.strip(), "%m/%d/%y %H:%M %p")
            # print(dt)
            # print('\n')
            return end
        else:
            return None

    def _parse_all_day(self, response):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, response):
        """Parse or generate location."""
        location = response.css("div.col-md-4 div.content-block p::text").getall()
        name = location[1]
        return {
            "address": "",
            "name": "",
        }

    def _parse_links(self, response):
        """Parse or generate links."""
        return [{"href": "", "title": ""}]

    # def _parse_source(self, response):
    #     """Parse or generate source."""
    #     return response.url
