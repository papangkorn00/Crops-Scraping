import scrapy
from crops_scraping.items import CropItemsBySeasons

class CropsSpider(scrapy.Spider):
    name = "crops"
    start_urls = ["https://coralisland.fandom.com/wiki/Crop"]

    def parse(self, response):
        season_map = {
            "Spring_crops": "Spring",
            "Summer_crops": "Summer",
            "Fall_crops": "Fall",
            "Winter_crops": "Winter"
        }

        for html_id, clean_season_name in season_map.items():
            target_table = response.xpath(f'//span[@id="{html_id}"]/../following-sibling::table[1]')

            for row in target_table.css('tbody tr'):
                if row.css('th'):
                    continue

                crop = CropItemsBySeasons()

                # season
                crop['season'] = clean_season_name

                # name
                crop['name'] = row.css('td:nth-child(1) a::text').get(default='').strip()

                # image_url
                crop['image_url'] = row.css('td:nth-child(1) span.custom-icon-image img::attr(data-src)').get()

                # town_rank
                crop['town_rank'] = row.css('td:nth-child(3)::text').get(default='').strip()

                # growth_time
                crop['growth_time'] = row.css('td:nth-child(4)::text').get(default='').strip()

                # seed_price
                crop['seed_price'] = row.css('td:nth-child(5)::attr(data-sort-value)').get()

                # sell_prices
                crop['sell_prices'] = row.css('td:nth-child(6)::attr(data-sort-value)').get()

                # possible_max_harvest
                crop['possible_max_harvest'] = row.css('td:nth-child(7)::text').get(default='').strip()

                yield crop


        

        
