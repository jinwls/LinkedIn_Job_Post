import scrapy
import string
import job.tidy as tidy
from job.tidy import TakeJob
from job.tidy import TakeOther
from job.tidy import TakeLocation
from job.tidy import StopwordRemove
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from itemloaders.processors import MapCompose
from scrapy.loader.processors import Identity
from w3lib.html import remove_tags




def remove_punc(value):
    return value.translate(str.maketrans('','',string.punctuation))

class JobItem(scrapy.Item):
    title      = scrapy.Field(input_processor = MapCompose(remove_tags, tidy.remove_whitespace, tidy.lower_case, tidy.remove_special), output_processor = TakeFirst())
    job        = scrapy.Field(input_processor = MapCompose(remove_tags, tidy.remove_whitespace, tidy.lower_case), output_processor = TakeJob())
    company    = scrapy.Field(input_processor = MapCompose(remove_tags, tidy.remove_whitespace, tidy.lower_case), output_processor = TakeFirst())
    city       = scrapy.Field(input_processor = MapCompose(remove_tags, tidy.remove_whitespace, tidy.lower_case), output_processor = TakeLocation().take_city)
    state      = scrapy.Field(input_processor = MapCompose(remove_tags, tidy.remove_whitespace, tidy.lower_case), output_processor = TakeLocation().take_states)
    date       = scrapy.Field(input_processor = MapCompose(remove_tags, tidy.remove_whitespace, tidy.remove_newlines), output_processor = TakeFirst())
    level      = scrapy.Field(input_processor = MapCompose(remove_tags, tidy.remove_whitespace, tidy.lower_case, tidy.remove_newlines), output_processor = TakeOther().take_level)
    type       = scrapy.Field(input_processor = MapCompose(remove_tags, tidy.remove_whitespace, tidy.lower_case, tidy.remove_newlines), output_processor = TakeOther().take_type)
    function   = scrapy.Field(input_processor = MapCompose(remove_tags, tidy.remove_whitespace, tidy.lower_case, tidy.remove_newlines), output_processor = TakeOther().take_function)
    industry   = scrapy.Field(input_processor = MapCompose(remove_tags, tidy.remove_whitespace, tidy.lower_case, tidy.remove_newlines), output_processor = TakeOther().take_industry)
    detail     = scrapy.Field(input_processor = MapCompose(remove_tags, remove_punc, tidy.remove_whitespace, tidy.remove_newlines, tidy.lower_case, tidy.remove_special, tidy.remove_accented, tidy.remove_repeat), output_processor = StopwordRemove())



# class JobItem(scrapy.Item):
#     title = scrapy.Field(input_processor = MapCompose(remove_tags, lower_case, remove_space, remove_punc), output_processor = TakeFirst())
#     company = scrapy.Field(input_processor = MapCompose(remove_tags, lower_case, remove_space), output_processor = TakeFirst())
#     location = scrapy.Field(input_processor = MapCompose(remove_tags, lower_case, remove_space), output_processor = TakeFirst())
#     crit_head = scrapy.Field(input_processor = MapCompose(lower_case, remove_space, remove_punc))
#     crit_text = scrapy.Field(input_processor = MapCompose(lower_case, remove_space, remove_punc))
#     detail = scrapy.Field(input_processor = MapCompose(lower_case, remove_space, remove_punc))
#     date = scrapy.Field(input_processor = MapCompose(remove_punc), output_processor = TakeFirst())    