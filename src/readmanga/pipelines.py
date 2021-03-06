from src.readmanga.images import ReadmangaImageSpider
from src.readmanga.items import ChapterImageList


class ReadmangaImagePipeline:
    """
    Readmanga image pipeline.

    Store images in redis with url of the chapter as the key.
    """

    @staticmethod
    def process_item(item: ChapterImageList, spider: ReadmangaImageSpider):
        spider.redis_client.json().set(spider.start_urls[0], "$", item["images"])  # type: ignore
        return item["images"]
