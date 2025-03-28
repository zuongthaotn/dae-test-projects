import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
from pathlib import Path
from scrapy import Selector


class IMDBUpcomingMoviesList(scrapy.Spider):
    name = "imdb_upcoming_movies"
    start_urls = ["https://m.imdb.com/calendar/?ref_=nv_mv_cal"]

    def parse(self, response):
        movies = []
        for movie_item in response.css(".ipc-metadata-list-summary-item__tc"):
            #
            movie_name = movie_item.css("a::text").get()
            #
            movie_path = movie_item.css("a::attr(href)").get()
            movie_id = movie_path.replace('/title/', '').replace('/?ref_=rlm', '')
            #
            movie_url = 'https://m.imdb.com/title/' + movie_id + '/?ref_=rlm'
            yield response.follow(url=movie_url, callback=self.parse_movie, meta={'movie_name': movie_name, 'movie_id': movie_id})

    def parse_movie(self, response):
        movie_id = response.meta.get('movie_id')
        name = response.meta.get('movie_name')
        error = False
        try:
            year = response.xpath("//ul[contains(@class, 'joVhBE')]/li/a/text()").get()
            duration = response.xpath("//ul[contains(@class, 'joVhBE')]/li/text()").get()
            interests = response.xpath("//a[contains(@class, 'ipc-chip--on-baseAlt')]/span/text()").getall()
            description = response.xpath("//p[contains(@class, 'NPkNd')]/span[1]/text()").get()
            dws_extra = response.xpath("//ul[contains(@class, 'ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt')]").getall()
        except Exception as e: 
            error = True
            return
        directors = []
        writers = []
        stars = []
        if len(dws_extra):
            try:
                directors = Selector(text=dws_extra[0]).xpath("//li/a/text()").getall()
                writers = Selector(text=dws_extra[1]).xpath("//li/a/text()").getall()
                stars = Selector(text=dws_extra[2]).xpath("//li/a/text()").getall()
            except Exception as e: 
                error = True
                return
        # top_cast = []
        # rating = 1
        # genres = []
        # countries_of_origin = []
        # language = []
        # withlist_text = 'Added by 3.5k users'
        # wishlist = 3500
        # test = 'https://m.imdb.com/title/tt11846550/?ref_=rlm'
        #
        if not error:
            csv_data = [{"ID": movie_id, "Name": name, "Year": year, "Duration": duration, "Interests": ','.join(str(x) for x in interests), "Description": description, 
                         "Directors": ','.join(str(x) for x in directors), "Writers": ','.join(str(x) for x in writers), "Stars": ','.join(str(x) for x in stars)
                         }]
            project_folder = Path(__file__).parent.parent
            df = pd.DataFrame(csv_data)
            df.to_csv(str(project_folder) + "/datasets/imdb_upcoming_movies.csv", mode='a', header=False, index=False)

def get_imdb_upcoming_movies():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        "LOG_ENABLED": False
    })
    process.crawl(IMDBUpcomingMoviesList)
    process.start()
