from typing import List

from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import CrawlSpider, Rule

from src import READMANGA_URL
from src.core.spider import WithOptionalUrl
from src.readmanga.items import MangaItem
from src.readmanga.spiders.list.utils import parse_rating

LIST_URL = f"{READMANGA_URL}/list"

MANGA_TILE_TAG = '//div[@class = "tiles row"]//div[contains(@class, "tile col-md-6")]'
STAR_RATE_TAG = '//div[@class = "rating"]/@title'
TITLE_TAG = "//h3/a[1]/@title"
SOURCE_URL_TAG = "//h3/a[1]/@href"
GENRES_TAG = '//div[@class = "tile-info"]//a[contains(@class, "badge")]/text()'
THUMBNAIL_IMG_URL_TAG = '//img[contains(@class, "lazy")][1]/@data-original'
ALT_TITLE_URL = "//h4[@title]//text()"


class ReadmangaListSpider(WithOptionalUrl, CrawlSpider):
    start_urls = [LIST_URL]
    rules = [
        Rule(
            LinkExtractor(restrict_xpaths=["//a[@class='nextLink']"]),
            follow=True,
            callback="parse",
        ),
    ]
    custom_settings = {
        "DEPTH_LIMIT": 400,
    }

    def parse_start_url(self, response, **kwargs):
        return self.parse(response, **kwargs)

    def parse(self, response: HtmlResponse, **kwargs):
        mangas: List[MangaItem] = []
        descriptions = response.xpath(MANGA_TILE_TAG).extract()
        for description in descriptions:
            response = HtmlResponse(url="", body=description, encoding="utf-8")

            rating = parse_rating(response.xpath(STAR_RATE_TAG).extract_first("")) / 2
            title = response.xpath(TITLE_TAG).extract_first("")
            source_url = response.xpath(SOURCE_URL_TAG).extract_first("")
            genres = response.xpath(GENRES_TAG).extract()
            thumbnail = response.xpath(THUMBNAIL_IMG_URL_TAG).extract_first("")
            image = thumbnail.replace("_p", "")
            alt_title = response.xpath(ALT_TITLE_URL).extract_first("")

            mangas.append(
                MangaItem(
                    **{
                        "rating": rating,
                        "title": title,
                        "alt_title": alt_title,
                        "thumbnail": thumbnail,
                        "image": image,
                        "genres": genres,
                        "source_url": READMANGA_URL + source_url,
                    }
                )
            )
            self.logger.info('Parsed manga "{}"'.format(title))

        self.logger.info("===================")
        return mangas
