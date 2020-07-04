from datetime import datetime, timedelta

import scrapy
from city_scrapers_core.constants import COMMITTEE
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from dateutil.relativedelta import relativedelta


class CcFinanceSpider(CityScrapersSpider):
    name = "cc_finance"
    agency = "Creve Coeur Finance Committee"
    timezone = "America/Chicago"

    def start_requests(self):
        today = datetime.now()
        for year_delta in range(-1, 2):
            year_str = (today + relativedelta(years=year_delta)).strftime("%Y")
            url = (
                "https://crevecoeurcitymo.iqm2.com/Citizens/Calendar"
                ".aspx?View=List&From=1/1/{year}&To=12/31/{year}".format(year=year_str)
            )
            yield scrapy.Request(url=url, method="GET", callback=self.parse)

    def parse(self, response):
        for url in self._get_event_urls(response):
            yield scrapy.Request(url, callback=self._parse_event, dont_filter=True)

    def _parse_event(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        times = self._parse_time(response)

        meeting = Meeting(
            title=self._parse_title(response),
            description=self._parse_description(response),
            classification=COMMITTEE,
            start=times[0],
            end=times[1],
            all_day=self._parse_all_day(response),
            time_notes=self._parse_time_notes(response),
            location=self._parse_location(response),
            links=self._parse_links(response),
            source=response.url,
        )

        meeting["status"] = self._get_status(meeting)
        meeting["id"] = self._get_id(meeting)

        return meeting

    def _get_event_urls(self, response):
        links = response.css("div.MeetingRow div.RowLink a::attr(href)").getall()
        details = response.css("div.MeetingRow div.RowDetails::text").getall()
        urls = []
        for link, detail in zip(links, details):
            if "finance" in detail.lower() and "committee" in detail.lower():
                urls.append(response.urljoin(link))
        return urls

    def _parse_title(self, response):
        """Parse or generate meeting title."""
        return response.css("span#ContentPlaceholder1_lblMeetingGroup::text").get()

    def _parse_description(self, response):
        """Parse or generate meeting description."""
        return "".join(response.css("span.MeetingCancelled::text").getall())

    def _parse_time(self, response):
        """Parse start and end datetime as a naive datetime object."""
        dt = response.css("span#ContentPlaceholder1_lblMeetingDate::text").get()
        start = datetime.strptime(dt.strip(), "%m/%d/%Y %H:%M %p")
        end = start + timedelta(hours=2)
        return (start, end)

    def _parse_time_notes(self, response):
        """Parse any additional notes on the timing of the meeting"""
        return ""

    def _parse_all_day(self, response):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, response):
        """Parse or generate location."""
        address = response.css("div.MeetingAddress::text").get().split("\xa0")
        address = " ".join(list(filter(lambda x: x != "", address)))
        text = response.css("td.MeetingHeading::text").getall()
        text = "".join(list(filter(lambda x: "\r\n" not in x, text))).strip()
        if "n/a" in address.lower():
            address = ""
        return {
            "address": address,
            "name": text,
        }

    def _parse_links(self, response):
        """Parse or generate links."""
        hrefs = response.css("div.MeetingDownloads a::attr(href)").getall()
        texts = response.css("div.MeetingDownloads a::text").getall()
        links = []
        for text, href in zip(texts, hrefs):
            if "agenda" in text.lower() and "packet" not in text.lower():
                links.append({"title": "Agenda", "href": response.urljoin(href)})
            if "minutes" in text.lower():
                links.append({"title": "Minutes", "href": response.urljoin(href)})
        return links
