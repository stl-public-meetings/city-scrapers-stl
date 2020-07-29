import re
from collections import defaultdict
from datetime import datetime

import scrapy
from city_scrapers_core.constants import BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.relativedelta import relativedelta


class ClayAldermenSpider(CityScrapersSpider):
    name = "clay_aldermen"
    agency = "Clayton Board of Aldermen"
    timezone = "America/Chicago"
    start_urls = [
        "https://www.claytonmo.gov/government/boards-and-commissions/board-of-aldermen"
    ]

    def __init__(self, *args, **kwargs):
        self.agenda_map = defaultdict(list)
        super().__init__(*args, **kwargs)

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        self._parse_links(response)
        yield from self._parse_meetings_page(response)

    def _parse_meetings_page(self, response):
        today = datetime.now()
        for month_delta in range(-1, 2):
            mo_str = (today + relativedelta(months=month_delta)).strftime("%m")
            yr_str = (today + relativedelta(months=month_delta)).strftime("%Y")
            url = (
                "https://www.claytonmo.gov/calendar-6/-curm-{month}/-cury-{year}"
            ).format(month=mo_str, year=yr_str)
            yield scrapy.Request(url=url, callback=self._parse_calendar_page)

    def _parse_calendar_page(self, response):

        for url in self._get_event_urls(response):
            yield scrapy.Request(url, callback=self._parse_event, dont_filter=True)

    def _get_event_urls(self, response):
        descriptions = response.css("div.calendar_item a::text").getall()
        links = response.css("div.calendar_item a::attr(href)").getall()

        urls = []

        for description, link in zip(descriptions, links):
            if "board of aldermen" in description.lower() or "BOA" in description:
                url = response.urljoin(link)

                pattern = r"(?P<link>.*/\d{4})"
                rm = re.search(pattern, url)

                if rm is not None:
                    urls.append(rm.group("link"))

        return urls

    def _parse_event(self, response):

        start = self._parse_start(response)
        links_key = datetime.strftime(start, "%m/%d/%Y")
        meeting = Meeting(
            title=self._parse_title(response),
            description="",
            classification=BOARD,
            start=self._parse_start(response),
            end=self._parse_end(response),
            all_day=False,
            location=self._parse_location(response),
            links=[],
            source=response.url,
        )

        if links_key in self.agenda_map.keys():
            meeting["links"] = self.agenda_map[links_key]
        else:
            meeting["links"] = []

        meeting["status"] = self._get_status(meeting)
        meeting["id"] = self._get_id(meeting)
        yield meeting

    def _parse_title(self, response):
        """Parse or generate meeting title."""
        return (
            response.css("h2.detail-title span::text")
            .get()
            .replace("BOA", "Board of Aldermen")
        )

    def _parse_start(self, response):
        """Parse start datetime as a naive datetime object."""
        date = response.css("span.detail-list-value::text").get()
        pattern = r"(?P<day>\d{2}/\d{2}/\d{4}) (?P<time>\d{1,2}:\d{2} (AM|PM)) - "
        pattern += r"\d{1,2}:\d{2} (AM|PM)"

        rm = re.search(pattern, date)

        if rm is not None:
            day = rm.group("day")
            time = rm.group("time")
            dt = day + " " + time
            start = datetime.strptime(dt.strip(), "%m/%d/%Y %H:%M %p")
            return start
        else:
            return None

    def _parse_end(self, response):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        date = response.css("span.detail-list-value::text").get()
        pattern = r"(?P<day>\d{2}/\d{2}/\d{4}) \d{1,2}:\d{2} (AM|PM) - "
        pattern += r"(?P<time>\d{1,2}:\d{2} (AM|PM))"

        rm = re.search(pattern, date)

        if rm is not None:
            day = rm.group("day")
            time = rm.group("time")
            dt = day + " " + time
            end = datetime.strptime(dt.strip(), "%m/%d/%Y %H:%M %p")
            return end
        else:
            return None

    def _parse_location(self, response):
        """Parse or generate location."""
        name = response.css(
            "span[itemprop='location'] span[itemprop='name']::text"
        ).get()
        address = response.css(
            "span[itemprop='location'] span[itemprop='address'] *::text"
        ).getall()
        address = " ".join(address).replace(" ,", ",").replace("  ", " ")
        return {
            "address": address,
            "name": name,
        }

    def _parse_links(self, response):
        """Parse or generate links."""
        rows = response.css("tr.meeting_widget_item *::attr(href)").getall()
        cells = response.css("tr.meeting_widget_item *::text").getall()

        dates = []
        for text in cells:
            pattern = r"(?P<date>\d{2}/\d{2}/\d{4})"
            rm = re.search(pattern, text)
            if rm is not None:
                date = rm.group("date")
                dates.append(date)

        dates_index = -1

        for row in rows:
            if "isPub" in row and dates_index in range(0, len(dates)):
                if dates[dates_index] not in self.agenda_map.keys():
                    self.agenda_map[dates[dates_index]] = [
                        {"href": response.urljoin(row), "title": "Agenda"}
                    ]
                else:
                    self.agenda_map[dates[dates_index]].append(
                        {"href": response.urljoin(row), "title": "Minutes"}
                    )
            else:
                dates_index += 1
            if dates_index > 6:
                break
