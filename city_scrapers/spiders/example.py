import re
from collections import defaultdict
from datetime import datetime

import scrapy
from city_scrapers_core.constants import BOARD, COMMITTEE, NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class StlAldermenSpider(CityScrapersSpider):
    name = "stl_public_service"
    agency = "St. Louis Board of Public Service"
    timezone = "America/Chicago"
    custom_settings = {"ROBOTSTXT_OBEY": False}
    start_urls = [
        (
            "https://www.stlouis-mo.gov/government/departments/public-service/index.cfm"
        )
    ]

    def __init__(self, *args, **kwargs):
        self.agenda_map = defaultdict(list)
        super().__init__(*args, **kwargs)

    def parse(self, response):
        self._parse_links(response)
        yield from self._parse_meetings_page(response)

    def _parse_meetings_page(self, response):
        urls = [
            (
                "https://www.stlouis-mo.gov/events/"
                "past-meetings.cfm?span=-30&department=332"
            ),
            "https://www.stlouis-mo.gov/events/all-public-meetings.cfm?span=30",
        ]
        for url in urls:
            yield scrapy.Request(
                url=url, method="GET", callback=self._parse_events_page
            )

    def _parse_events_page(self, response):
        for url in self._get_event_urls(response):
            yield scrapy.Request(url, callback=self._parse_event, dont_filter=True)

    def _get_event_urls(self, response):
        event_urls = response.css("ul.list-group h4 a::attr(href)").getall()
        event_sponsors = response.css("ul.list-group li span.small::text").getall()
        urls = []
        for url, sponsor in zip(event_urls, event_sponsors):
            if "aldermen" in sponsor.lower() or "aldermanic" in sponsor.lower():
                urls.append(response.urljoin(url))
        return urls

    def _parse_event(self, response):
        """
        `parse` should always `yield` Meeting items.
        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        start = self._parse_start(response)
        links_key = datetime.strftime(start, "%m-%d-%y")

        meeting = Meeting(
            title=self._parse_title(response),
            description=self._parse_description(response),
            classification=self._parse_classification(response),
            start=start,
            end=self._parse_end(response),
            all_day=self._parse_all_day(response),
            location=self._parse_location(response),
            source=response.url,
        )

        if meeting["classification"] == BOARD:
            if links_key in self.agenda_map.keys():
                meeting["links"] = self.agenda_map[links_key]
        else:
            meeting["links"] = []

        meeting["status"] = self._get_status(meeting)
        meeting["id"] = self._get_id(meeting)
        return meeting

    def _parse_title(self, response):
        """Parse or generate meeting title."""
        title = response.css("div.page-title-row h1::text").get()
        title = title.replace("Meeting", "").replace("Metting", "")
        title = title.replace("-", "- ")
        title = title.replace("(Canceled)", "Cancelled")
        return title.replace("  ", " ").strip()

    def _parse_description(self, response):
        """Parse or generate meeting description."""
        description = response.css(
            "div#EventDisplayBlock div.col-md-8 h4 strong::text"
        ).getall()
        i = 0
        while i < len(description) - 1:
            if "following:" in description[i]:
                return description[i + 1].replace("\xa0", "")
            elif "will" in description[i]:
                return description[i].replace("\xa0", "")
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
        else:
            name = ""
            address = ""

        return {
            "address": address,
            "name": name,
        }

    def _parse_links(self, response):
        """Parse or generate links."""
        rows = response.css("table.data tr")
        for row in rows:

            temp_links = []
            link = row.css("a::attr(href)").getall()
            description = row.css("td *::text").getall()
            description = "".join(description).replace("\n", " ")

            pattern_mmddyy = r"(?P<date>(\d{1,2}-\d{1,2}-\d{2}))"
            pattern_mmddyyyy = r"(?P<date>(\d{1,2}-\d{1,2}-\d{4}))"
            pattern_monthddyyyy = r"(?P<date>([A-Z]* \d{1,2}, \d{4}))"

            rm_mmddyy = re.search(pattern_mmddyy, description)
            rm_mmddyyyy = re.search(pattern_mmddyyyy, description)
            rm_monthddyyyy = re.search(pattern_monthddyyyy, description)

            dt = None
            if rm_mmddyy is not None:
                date = rm_mmddyy.group("date")
                dt = datetime.strptime(date, "%m-%d-%y")
            if rm_mmddyyyy is not None:
                date = rm_mmddyyyy.group("date")
                dt = datetime.strptime(date, "%m-%d-%Y")
            if rm_monthddyyyy is not None:
                date = rm_monthddyyyy.group("date")
                dt = datetime.strptime(date, "%b %d, %Y")

            if dt is not None:
                formatted_date = datetime.strftime(dt, "%m-%d-%y")
                if len(link) >= 2:
                    temp_links.append(
                        {"href": response.urljoin(link[1]), "title": "Agenda"}
                    )
                if len(link) == 3:
                    temp_links.append(
                        {"href": response.urljoin(link[2]), "title": "Minutes"}
                    )

                self.agenda_map[formatted_date] = temp_links
