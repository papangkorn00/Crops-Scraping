import scrapy

class CropItemsBySeasons(scrapy.Item):
    season = scrapy.Field()
    name = scrapy.Field()
    town_rank = scrapy.Field()
    growth_time = scrapy.Field()
    re_growth_time = scrapy.Field()
    seed_price = scrapy.Field()
    sell_prices = scrapy.Field()
    possible_max_harvest = scrapy.Field()
    image_url = scrapy.Field()