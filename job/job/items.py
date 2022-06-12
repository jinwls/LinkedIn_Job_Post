import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


def lower_space(value):
    # value = value.extract()
    return value.strip().lower()

def lower_case(value):
    return value.lower()

class JobItem(scrapy.Item):
    title = scrapy.Field(input_processor = MapCompose(remove_tags, lower_space), output_processor = TakeFirst())
    company = scrapy.Field(input_processor = MapCompose(remove_tags, lower_space), output_processor = TakeFirst())
    location = scrapy.Field(input_processor = MapCompose(remove_tags, lower_space), output_processor = TakeFirst())
    crit_head = scrapy.Field(input_processor = MapCompose(lower_space))
    crit_text = scrapy.Field(input_processor = MapCompose(lower_space))
    detail = scrapy.Field(input_processor = MapCompose(lower_space))
    date = scrapy.Field(input_processor = MapCompose(lower_space), output_processor = TakeFirst())