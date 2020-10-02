from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider
from datetime import datetime


class ClayUniformRetirementSpider(CityScrapersSpider):
    name = "clay_uniform_retirement"
    agency = "Clayton Uniformed Emlpoyees Retirement Board"
    timezone = "America/Chicago"
    start_urls = [
        "https://www.claytonmo.gov/government/\
        boards-and-commissions/uniformed-employees-retirement-board"
    ]
    address = "Missouri"

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.css("table"):
            meeting = Meeting(
                title=self._parse_title(response),
                description=self._parse_description(item),
                classification=self._parse_classification(item),
                start=self._parse_start(response),
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

    def _parse_title(self, item):
        """Parse or generate meeting title."""
        title = item.css("tbody tr td a::text").extract_first()
        return title

    def _parse_description(self, item):
        """Parse or generate meeting description."""
        return ""

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return "BOARD"

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        date_time = item.css("tbody tr .mobile_hide::text").extract_first()
        date_time = datetime.strptime(date_time, "%d/%m/%Y %H:%M %p")
        return date_time

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return ""

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, item):
        """Parse or generate location."""
        return {
            "address": self.address,
            "name": "",
        }

    def _parse_links(self, item):
        """Parse or generate links."""
        host_link = "https://www.claytonmo.gov"
        links = item.css("td span a::attr('href')").extract()
        l = []
        for agenda_minutes in links:
            l.append(
                {"href": host_link + agenda_minutes, "title": agenda_minutes[33:46]}
            )
        return l

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
