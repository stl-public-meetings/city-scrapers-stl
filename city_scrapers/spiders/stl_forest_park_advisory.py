import re
from collections import defaultdict
from datetime import datetime

import scrapy
from city_scrapers_core.constants import BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider


class StlForestParkAdvisory(CityScrapersSpider):
    name = "stl_forest_park_advisory"
    agency = "Parks, Recreation and Forestry"
    timezone = "America/Chicago"
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def __init__(self, *args, **kwargs):
        self.agenda_map = defaultdict(list)
        self.minute_map = defaultdict(list)
        super().__init__(*args, **kwargs)

    def start_requests(self):
        agenda_url = (
            "https://sites.google.com/a/stlouis-mo.gov/forest-park-master-plan/home"
        )
        yield scrapy.Request(
            url=agenda_url, method="GET", callback=self._get_agenda_urls, priority=100
        )
        yield scrapy.Request(
            url=agenda_url, method="GET", callback=self._get_minute_urls, priority=100
        )

        meeting_urls = [
            (
                "https://www.stlouis-mo.gov/government/departments"
                "/parks/parks/forest-park-advisory-board.cfm"
            ),
            ("https://www.stlouis-mo.gov/events/past-meetings.cfm?department=117"),
        ]
        for url in meeting_urls:
            yield scrapy.Request(url=url, method="GET", callback=self.parse)

    def parse(self, response):
        for url in self._get_event_urls(response):
            yield scrapy.Request(url=url, callback=self._parse_event)

    def _get_event_urls(self, response):
        event_titles = response.xpath(
            '//*/a[contains(@href, "Event_ID")]/strong/text()'
        ).getall()
        if len(event_titles) == 0:
            event_titles = response.xpath(
                '//*/a[contains(@href, "Event_ID")]/text()'
            ).getall()
        event_urls = response.xpath('//*/a[contains(@href, "Event_ID")]/@href').getall()
        urls = []
        for url, title in zip(event_urls, event_titles):
            if "Forest Park Advisory" in title:
                urls.append(response.urljoin(url))
        return urls

    def _parse_event(self, response):

        start = self._parse_start(response)
        links_key = datetime.strftime(start, "%Y-%m-%d")

        meeting = Meeting(
            title=self._parse_title(response),
            description=self._parse_desc(response),
            classification=BOARD,
            start=start,
            end=self._parse_end(response),
            all_day=False,
            location=self._parse_location(response),
            source=response.url,
        )

        meeting["links"] = []

        if links_key in self.agenda_map.keys():
            meeting["links"].append(self.agenda_map[links_key])

        if links_key in self.minute_map.keys():
            meeting["links"].append(self.minute_map[links_key])

        return meeting

    def _parse_start(self, response):
        date = response.xpath('//*/p[@class="page-summary"]/text()').get()
        date = date.replace("\n", "")
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

    def _parse_title(self, response):
        title = response.xpath('//*/div[@class="EventTitle"]/text()').get()
        title = title.replace("\n", "")

        return title

    def _parse_desc(self, response):
        descs = response.xpath(
            '//*/div[@id="EventDisplayBlock"]/div[@class="row"]/div/p/text()'
        ).getall()
        description = ""
        for desc in descs:
            if desc == "\n":
                desc = ""
            else:
                desc = desc.replace("\xa0", "")
                desc = desc.replace("\n", "")
            description = description + desc

        return description

    def _parse_end(self, response):
        date = response.xpath('//*/p[@class="page-summary"]/text()').get()
        date = date.replace("\n", "")
        pattern = r"(?P<day>\d{2}/\d{2}/\d{2}), (\d{1,2}:\d{2}) (PM|AM)"
        pattern += r" - (?P<time>(\d{1,2}:\d{2}) (PM|AM))"
        rm = re.search(pattern, date)

        if rm is not None:
            day = rm.group("day")
            time = rm.group("time")
            dt = day + " " + time
            start = datetime.strptime(dt.strip(), "%m/%d/%y %H:%M %p")
            return start
        else:
            return None

    def _parse_location(self, response):
        title = response.xpath('//*/div[@class="EventTitle"]/text()').get()
        meeting_type = response.xpath('//*/div[@class="MeetingType"]/text()').get()

        if "zoom" in title.lower() or "zoom" in meeting_type.lower():
            name = "Zoom"
            address = ""
        else:
            infos = response.xpath(
                '//*/strong[text()="Location:"]/parent::p/text()'
            ).getall()
            address = infos[-2].replace("\n", "") + ", " + infos[-1].replace("\n", "")
            name = infos[-3].replace("\n", "")

        return {"address": address, "name": name}

    def _get_agenda_urls(self, response):
        links = response.xpath(
            '//*/a[contains(@href, "FPAB") and contains(@href, "Agenda")]/@href'
        ).getall()
        titles = response.xpath(
            '//*/span[@class="td-value" and contains(text(), "FPAB Agenda")]/text()'
        ).getall()

        for link, title in zip(links, titles):
            if "CANCELLED" not in title:
                url = response.urljoin(link)
                date = re.search(r"([0-9]{4}\-[0-9]{2}\-[0-9]{2})", title)[0]
                link_obj = {"href": url, "title": title}
                self.agenda_map[date] = link_obj

    def _get_minute_urls(self, response):
        links = response.xpath(
            '//*/a[contains(@href, "FPAB") and contains(@href, "Minutes")]/@href'
        ).getall()
        titles = response.xpath(
            '//*/span[@class="td-value" and contains(text(), "FPAB Minutes")]/text()'
        ).getall()

        for link, title in zip(links, titles):
            if "NONE" not in title:
                url = response.urljoin(link)
                date = re.search(r"([0-9]{4}\-[0-9]{2}\-[0-9]{2})", title)[0]
                link_obj = {"href": url, "title": title}
                self.minute_map[date] = link_obj
