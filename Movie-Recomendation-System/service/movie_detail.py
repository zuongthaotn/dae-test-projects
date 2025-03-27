import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
from pathlib import Path


def get_movie_urls():
    current_folder = Path(__file__).parent
    df = pd.read_csv(str(current_folder) + "/imdb_upcoming_movies.csv")
    urls = []
    for i, row in df.iterrows():
        movie_url = 'https://m.imdb.com/title/' + row['ID'] + '/?ref_=rlm'
        urls.append(movie_url)
    return urls


class IMDBMovideDetail(scrapy.Spider):
    name = "metadata_imdb_upcoming_movies"
    start_urls = get_movie_urls()

    def parse(self, response):
        name = response.xpath("//h1/span/text()").get()
        print(name)
        year = response.xpath("//ul[contains(@class, 'joVhBE')]/li/a/text()").get()
        duration = response.xpath("//ul[contains(@class, 'joVhBE')]/li/text()").get()
        interests = response.xpath("//a[contains(@class, 'ipc-chip--on-baseAlt')]/span/text()").getall()
        description = response.xpath("//p[contains(@class, 'NPkNd')]/span[1]/text()").get()
        dws_extra = response.xpath("//ul[contains(@class, 'ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt')]").getall()
        directors = []
        writers = []
        stars = []
        if len(dws_extra):
            directors = dws_extra[0].xpath("//li/a/text()").getall()
            writers = dws_extra[1].xpath("//li/a/text()").getall()
            stars = dws_extra[2].xpath("//li/a/text()").getall()
        top_cast = []
        rating = 1
        genres = []
        countries_of_origin = []
        language = []
        withlist_text = 'Added by 3.5k users'
        wishlist = 3500
        test = 'https://m.imdb.com/title/tt11846550/?ref_=rlm'
        #
        if name:
            csv_data = [{"Name": name, "Year": year, "Duration": duration, "Interests": ', '.join(str(x) for x in interests), "Description": description, 
                         "Directors": ', '.join(str(x) for x in directors), "Writers": ', '.join(str(x) for x in writers), "Stars": ', '.join(str(x) for x in stars)
                         }]
            current_folder = Path(__file__).parent
            df = pd.DataFrame(csv_data)
            df.to_csv(str(current_folder) + "/imdb_upcoming_movies_extra.csv", mode='a', header=False, index=False)

def get_detail_movies():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        "LOG_ENABLED": False
    })
    process.crawl(IMDBMovideDetail)
    process.start()

get_detail_movies()