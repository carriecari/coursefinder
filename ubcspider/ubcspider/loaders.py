from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Identity, TakeFirst
from w3lib.html import remove_tags


class CourseLoader(ItemLoader):
    # default_input_processor = MapCompose(remove_tags, str.strip)
    # default_output_processor = TakeFirst()
    name_in = MapCompose(remove_tags, str.strip)
    prereqs_out = MapCompose(remove_tags, str.strip)

    name_out = TakeFirst()
    default_output_processor = Identity()
    oneOf_out = Identity()
    eitherOr_out = Identity()
