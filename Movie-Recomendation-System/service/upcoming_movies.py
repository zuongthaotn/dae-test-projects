import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
from pathlib import Path


class IMDBUpcomingMoviesList(scrapy.Spider):
    name = "imdb_upcoming_movies"
    start_urls = ["https://m.imdb.com/calendar/?ref_=nv_mv_cal"]

    def parse(self, response):
        movies = []
        for movie_item in response.css(".ipc-metadata-list-summary-item__tc"):
            #
            movie_name = movie_item.css("a::text").get()
            #
            movie_url = movie_item.css("a::attr(href)").get()
            movie_id = movie_url.replace('/title/', '').replace('/?ref_=rlm', '')
            #
            movies.append({"ID": movie_id, "title": movie_name})
        #
        current_folder = Path(__file__).parent
        df = pd.DataFrame(movies)
        df.to_csv(str(current_folder) + "/imdb_upcoming_movies.csv", index=False)
        print("Data saved to imdb_upcoming_movies.csv")

def get_imdb_upcoming_movies():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        "LOG_ENABLED": False
    })
    process.crawl(IMDBUpcomingMoviesList)
    process.start()

# get_imdb_upcoming_movies()