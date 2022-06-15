import scrapy
import string
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from scrapy.loader.processors import MapCompose
from scrapy.loader.processors import Identity
from w3lib.html import remove_tags


# def lower_space_punc(value):
#     # value = value.extract()
#     return value.strip().lower().translate(str.maketrans('', '', string.punctuation))

def lower_case(value):
    return value.lower()

def remove_space(value):
    return value.strip()

def remove_punc(value):
    return value.translate(str.maketrans('','',string.punctuation))

class JobItem(scrapy.Item):
    title = scrapy.Field(input_processor = MapCompose(remove_tags, lower_case, remove_space, remove_punc), output_processor = TakeFirst())
    company = scrapy.Field(input_processor = MapCompose(remove_tags, lower_case, remove_space), output_processor = TakeFirst())
    location = scrapy.Field(input_processor = MapCompose(remove_tags, lower_case, remove_space), output_processor = TakeFirst())
    crit_head = scrapy.Field(input_processor = MapCompose(lower_case, remove_space, remove_punc))
    crit_text = scrapy.Field(input_processor = MapCompose(lower_case, remove_space, remove_punc))
    detail = scrapy.Field(input_processor = MapCompose(lower_case, remove_space, remove_punc))
    date = scrapy.Field(input_processor = MapCompose(remove_punc), output_processor = TakeFirst())    