import re
from collections import defaultdict
from datetime import datetime

import scrapy
from city_scrapers_core.constants import BOARD
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider

class StlForestParkAdvisorySpider(CityScrapersSpider):
    name = "stl_forest_park_advisory"
    agency = "Parks, Recreation and Forestry"
    timezone = "America/Chicago"
    custom_settings = {"ROBOTSTXT_OBEY": False}

    def __init__(self, *args, **kwargs):
        self.agenda_map = defaultdict(list)
        super().__init__(*args, **kwargs)
    
    def start_requests(self):
        meeting_urls = [
            (
                "https://www.stlouis-mo.gov/government/departments"
                "/parks/parks/forest-park-advisory-board.cfm"
            ),
            (
                "https://www.stlouis-mo.gov/events/past-meetings.cfm"
                "?meetingType=All+Meetings&department=117&span=-60"
            ),
        ]
        for url in meeting_urls:
            yield scrapy.Request(url=url, method="GET", callback=self.parse, priority=100)
        
        agenda_url = (
            "https://sites.google.com/a/stlouis-mo.gov/forest-park-master-plan/home"
        )
        yield scrapy.Request(url=agenda_url, method="GET", callback=self._get_agenda_urls)

    def parse(self, response):
        

