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
        self.url = "https://www.coursera.org/courses?query=data%20engineering&language=English&productTypeDescription=Courses&topic=Information%20Technology"

    def start_requests(self):
        url = f"{self.url}&page={self.page}"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        script_data = response.xpath('//script[contains(text(), "searchResults")]').get()
        if not script_data:
            self.logger.warning("No data found.")
            self.stop = True
            return
        print(f"---------------{self.page}---------------")
        product_cards = re.split(r'(?=,"ProductCard_ProductCard:)', script_data)
        print(f"Number of product cards: {len(product_cards)}")
        results = []
        for product_card in product_cards:
            if ',"ProductCard_ProductCard:' in product_card:
                results.append(product_card)
        results[-1] = process_latest_string(results[-1])
        for item in results:
            item = item[1:]
            item = '{' + item + '}'
            item = json.loads(item)
            for key, value in item.items():
                if value.get("__typename") == "Search_ProductHit":
                    # if self.page == 1 or self.page == 2:
                    #     print(value.get("name"))
                    if value.get("isCourseFree") == True:
                        yield {
                            "page": self.page,
                            "title": value.get("name"),
                            "is_free": value.get("isCourseFree"),
                            "url": "https://www.coursera.org" + value.get("url", ""),
                            "skills": ','.join(value.get("skills"))
                        }
        item = []
        if not self.stop:
            self.page += 1
            next_page_url = f"{self.url}&page={self.page}"
            # print(next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse)


# Inline run bằng CrawlerProcess
if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "FEEDS": {
            "courses.csv": {"format": "csv", "overwrite": True},
        },
        'DOWNLOAD_TIMEOUT': 4,
        'RETRY_TIMES': 1,
        "LOG_ENABLED": False
    })

    process.crawl(DataEngineeringCourses)
    process.start()
