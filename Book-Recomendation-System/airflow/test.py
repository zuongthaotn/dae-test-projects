import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
from pathlib import Path
from scrapy import Selector
import re
import time


class NewReleasedBooks(scrapy.Spider):
    name = "new_release_books"
    allowed_domains = ["goodreads.com"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = 1
        self.stop = False
        self.ids = []
        self.init_url = "https://www.goodreads.com/shelf/show/2025-releases"

    def start_requests(self):
        url = f"{self.init_url}?page={self.page}"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        # self.logger.info(f"Parsing page: {response.url}")
        book_data = []
        try:
            local_dir = Path(__file__).parent
            books = response.xpath('//div[@class="elementList"]')
            print(f"Parsing page: {response.url}")
            print(f"Len response: {len(response.text)}")
            with open(f"{local_dir}/response-{self.page}.txt", "w", encoding="utf-8") as f:
                f.write(response.text)
                # f.write(str(books.getall()))
            
            # for book in books:
            #     title = book.css('a.bookTitle::text').get()
            #     link = response.urljoin(book.css('a.bookTitle::attr(href)').get())
            #     yield {
            #         'title': title,
            #         'link': link
            #     }
            #     book_data.append(f"{title}, {link}")
            if not len(books):
                self.stop = True
        except Exception as e: 
            print(e)
            return
        #
        # if book_data:
        #     print('---ok------')
        #     with open("book-list.txt", "a", encoding="utf-8") as f:
        #         f.write("\n".join(book_data) + "\n")
        #
        if self.page > 3:
            return
        if not self.stop:
            self.page += 1
            next_page = f"{self.init_url}?page={self.page}"
            cookies = {
                "ccsid": "037-5933792-1100514",
                "csm-sid": "704-9167167-1034410",
                "logged_out_browsing_page_count": "2",
                "session-id": "137-6886985-8724525",
                "ubid-main": "133-1203895-0328038",
                "csm-hit": "tb:s-0XK2XT2E6G420TYG6W2A|1746617333421&t:1746617333422",
                "session-id-time": "2377337355l",
                "session-token": "\"2nqOu3UkySrG3Lz19t3wwFJbPetutAm9dWYmfdtAiB4ltwACHumKcahNuMmApptEQf6nUMg3fVLfrpMiE+/dqn96RSzsyy83k8O2dHUH6WpJd5wG2IYJuOrcpwSLjtnagQXlYK4g0SxvXC1o3FByXkPN6e6svWR9/oYzrftWXpD4gywnZXvZk1Rxrp9QrJZmDrJQj9RiycBnIMjCPlBs+le2ngH8WxlNiia7f1Cq2Tt3aDa8UrQHNZiNGPF9T82p3CcJGtpc6OgUYPKCP562yYgfd/Ie2MaN3/PWPz4YPxCw0cmQNvKkA7D+XBGopJcRN+g0Bh9KfXdAuHb1ttjaD/Imu2uzlmt8sylcrMKZ9Q3Zg3UwyaKh5w",
                "x-main": "\"BXcO98AxW2@5oN@jwPtmWMDoK8iWi@476x5s0Msq8iF0OkiOv1CZhct3erwL5F6d\"",
                "at-main": "Atza|IwEBIAUFvcf0GHJpg_qqIkSBVvaMg5CAJ5u_JLsKzbxku6x3bKLGkfCzGHh4WzMVU6wbHkfCMv3YqPQ7ywJqBG2CeeYWMpPjxCDPayZoKObUVSMBv-Mtga8sdKD9qMiKYN_3fBjZJDtUXaFEc5zw0on5pamIWjOuvRteiY5XYw8-FPhZpZkoFgF47nLDiuEtfTY9aFRo4JmCAx6tBx6GQ8F4Tp5HHK764vmU1uUL1gj1yr9YiUA0QJ9PHAU4IzFYxDZfvbM",
                "sess-at-main": "\"v+Ujiu1NITvqr2ohzU2hdzFyHFQv9ik1tL9AiBiCfXA",
                "likely_has_account": "true",
                "__gads": "ID",
                "__gpi": "UID",
                "__eoi": "ID",
                "locale": "en",
                "_session_id2": "dbd92d88973d1106261d92ca82d49378"
            }
            yield scrapy.Request(next_page, callback=self.parse, cookies=cookies)
            # yield response.follow(next_page, callback=self.parse)
        #

if __name__ == "__main__":
    local_dir = Path(__file__).parent
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        # "FEEDS": {
        #     str(local_dir)+"/book-list.csv": {"format": "csv", "overwrite": True},
        # },
        'DOWNLOAD_TIMEOUT': 4,
        'RETRY_TIMES': 1,
        'HTTPCACHE_ENABLED': False,
        # 'DUPEFILTER_DEBUG': True,
        "LOG_ENABLED": False
    })

    process.crawl(NewReleasedBooks)
    process.start()
