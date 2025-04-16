import scrapy
from scrapy.crawler import CrawlerProcess
import re
import json


def process_latest_string(str):
    idx = str.find(',"SearchResultQueries:{}"')
    if idx != -1:
        needed = str[:idx]
    else:
        needed = str
    return needed

def get_str_before_str(str):
    idx = str.find('{"__typename":')
    if idx != -1:
        needed = str[idx:]
    else:
        needed = str
    return needed


class DataEngineeringCourses(scrapy.Spider):
    name = "coursera_inline"
    allowed_domains = ["coursera.org"]

    def __init__(self, keyword="data engineering", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = 1
        self.stop = False
        self.ids = []
        self.url = "https://www.coursera.org/courses?query=data%20engineering&language=English&productTypeDescription=Courses&topic=Computer%20Science&topic=Data%20Science&topic=Information%20Technology"

    def start_requests(self):
        url = f"{self.url}&page={self.page}"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        script_data = response.xpath('//script[contains(text(), "searchResults")]').get()
        if not script_data:
            self.logger.warning("No data found.")
            self.stop = True
            return
        match = re.search(r'window\.__APOLLO_STATE__\s*=\s*(.*?)window\.renderedClassNames', script_data, re.DOTALL)
        if not match:
            print("Search result not found")
            self.stop = True
            return
        extracted = match.group(1).strip()
        json_str = extracted.rstrip(";")
        data = json.loads(json_str)
        #
        product_hits = []
        search_results = []
        for key, value in data.items():
            if key == "SearchResultQueries:{}":
                for key2, value2 in value.items():
                    if 'search' in key2 and isinstance(value2, list) and len(value2):
                        if isinstance(value2[0]['elements'], list):
                            for element in value2[0]['elements']:
                                search_results.append(element['__ref'])                        
            elif isinstance(value, dict) and value.get("__typename") == "Search_ProductHit":
                value["Search_ProductHit"] = key
                product_hits.append(value)
        #
        if not len(search_results):
            print(f"No item found. Stopped at page {self.page}")
            self.stop = True
            return
        #
        for product_hit in product_hits:
            if product_hit.get("isCourseFree") == True and product_hit.get("Search_ProductHit") in search_results:
                if product_hit.get("id") not in self.ids:
                    yield {
                        "page": self.page,
                        "title": product_hit.get("name"),
                        "is_free": product_hit.get("isCourseFree"),
                        "url": "https://www.coursera.org" + product_hit.get("url", ""),
                        "skills": ','.join(product_hit.get("skills"))
                    }
                    self.ids.append(product_hit.get("id"))

        #
        if not self.stop:
            self.page += 1
            next_page_url = f"{self.url}&page={self.page}"
            yield scrapy.Request(next_page_url, callback=self.parse)


if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEEDS": {
            "free-courses.csv": {"format": "csv", "overwrite": True},
        },
        'DOWNLOAD_TIMEOUT': 4,
        'RETRY_TIMES': 1,
        "LOG_ENABLED": False
    })

    process.crawl(DataEngineeringCourses)
    process.start()
