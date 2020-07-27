import re
from collections import defaultdict
from datetime import datetime

import scrapy
from city_scrapers_core.constants import BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider

#
class StlPublicService(CityScrapersSpider):
    name = "stl_public_service"
    agency = "St. Louis Board of Public Service"
    timezone = "America/Chicago"
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def __init__(self, *args, **kwargs):
        self.agenda_map_service = defaultdict(list)
        super().__init__(*args, **kwargs)

    def start_requests(self):
        calendar_urls = [
            (
                "https://www.stlouis-mo.gov/events/"
                "past-meetings.cfm?span=-30&department=209"
            ),
            "https://www.stlouis-mo.gov/events/all-public-meetings.cfm?span=30",
        ]
        for url in calendar_urls:
            yield scrapy.Request(url=url, method="GET", callback=self.parse)

    def parse(self, response):
        for url in self._get_event_urls(response):
            yield scrapy.Request(url, callback=self._parse_event, dont_filter=True)

    def _get_event_urls(self, response):
        event_urls = response.css("ul.list-group h4 a::attr(href)").getall()
        event_sponsors = response.css("ul.list-group li span.small::text").getall()
        urls = []
        for url, sponsor in zip(event_urls, event_sponsors):
            if "public service" in sponsor.lower():
                urls.append(response.urljoin(url))
        return urls

    def _get_agenda_urls(self, response):
        urls = response.css("td.CS_PgIndex_Item a::attr(href)").getall()[:3]
        urls += response.css("td.CS_PgIndex_Item_Alternate a::attr(href)").getall()[:3]
        for url in urls:
            yield scrapy.Request(
                url=response.urljoin(url),
                method="GET",
                callback=self._parse_links,
                dont_filter=True,
            )

    def _parse_event(self, response):
        """
        return Meeting items.
        """
        start = self._parse_start(response)
        links_key = datetime.strftime(start, "%m-%d")

        meeting = Meeting(
            title=self._parse_title(response),
            description="",
            classification=BOARD,
            start=start,
            end=self._parse_end(response),
            all_day=self._parse_all_day(response),
            location=self._parse_location(response),
            source=response.url,
        )

        meeting["links"] = []
        if "public service" in meeting["title"].lower():
            if links_key in self.agenda_map_service.keys():
                meeting["links"] = self.agenda_map_service[links_key]

        meeting["status"] = self._get_status(meeting)
        meeting["id"] = self._get_id(meeting)
        return meeting

    def _parse_title(self, response):
        """Parse or generate meeting title."""
        title = response.css("div.page-title-row h1::text").get()
        return title.strip()

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

    def _parse_all_day(self, response):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, response):
        """Parse or generate location."""
        location = response.css("div.col-md-4 div.content-block p *::text").getall()
        temp = []
        for item in location:
            item = item.replace("\n", "")
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

        if location_index + 1 < len(location) and sponsor_index < len(location):
            name = location[location_index + 1]
            address = []
            for j in range(location_index + 2, sponsor_index):
                address.append(location[j])
            address = (
                " ".join(address).replace("Directions to this address", "").strip()
            )
            address = address.replace(", ", ",").replace(",", ", ")
        else:
            name = ""
            address = ""

        return {
            "address": address,
            "name": name,
        }

    def _parse_links(self, response):
        """Parse or generate links."""
        agency = response.css("div.cs_control h1::text").get()
        links = response.css("div.download li a::attr(href)").getall()
        descriptions = response.css("div.download li a::text").getall()

        for description, link in zip(descriptions, links):

            pattern_monthdd = r"(?P<date>[A-Z][a-z]* \d{1,2})"
            pattern_month_dd = r"(?P<date>[A-Z][a-z]*-\d{1,2})"

            rm_monthdd = re.search(pattern_monthdd, description)
            rm_month_dd = re.search(pattern_month_dd, description)

            dt = None
            if rm_monthdd is not None:
                date = rm_monthdd.group("date")
                dt = datetime.strptime(date, "%B %d")
            if rm_month_dd is not None:
                date = rm_month_dd.group("date")
                dt = datetime.strptime(date, "%B-%d")

            if dt is not None:
                formatted_date = datetime.strftime(dt, "%m-%d")
                if "adjustment" in agency.lower():
                    self.agenda_map_adjustment[formatted_date] = [
                        {"href": response.urljoin(link), "title": "Agenda"}
                    ]
                if "conditional" in agency.lower():
                    self.agenda_map_conditional[formatted_date] = [
                        {"href": response.urljoin(link), "title": "Agenda"}
                    ]
