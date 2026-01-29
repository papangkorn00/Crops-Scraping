
# import json
import psycopg2
import os 
from dotenv import load_dotenv

# class CropsScrapingPipeline:
#     def process_item(self, item):
#         return item
    
# class MultiSeasonFilterPipeline:
#     def open_spider(self):
#         self.crop_map = {}

#     def process_item(self, item):
#         name = item['name']
#         season = item['season']

#         try:
#             base_price = float(item.get('sell_prices', 0))
#         except (ValueError, TypeError):
#             base_price = 0

#         price_dict = {
#             "Base": int(base_price * 1),
#             "Bronze": int(round(base_price * 1.15)),
#             "Silver": int(round(base_price * 1.30)),
#             "Gold": int(round(base_price * 1.50)),
#             "Osmium": int(round(base_price * 2.00))
#         }

#         if name in self.crop_map:
#             if season not in self.crop_map[name]['seasons']:
#                 self.crop_map[name]['seasons'].append(season)
#         else:
#             crop_dict = dict(item)
#             crop_dict['seasons'] = [season]

#             crop_dict['sell_prices'] = price_dict

#             if 'season' in crop_dict:
#                 del crop_dict['season']

#             self.crop_map[name] = crop_dict
#         return item
    
#     def close_spider(self):
#         all_crops = []

#         for data in self.crop_map.values():
            
#             all_crops.append(data)

#         with open('all_seasons_crops.json', 'w', encoding='utf-8') as f:
#             json.dump(all_crops, f, indent=4, ensure_ascii=False)

load_dotenv()

class SaveToPostgresPipeline:
    def open_spider(self):
        # connect to db
        self.connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),          
            password=os.getenv("DB_PASSWORD")
        )
        self.cur = self.connection.cursor()
        
        # --- LOAD SQL FILE LOGIC ---
        # 1. Get the folder where THIS file (pipelines.py) is located
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # 2. Build the full path to the SQL file
        sql_path = os.path.join(base_dir, 'sql_queries', 'upsert_crop.sql')
        
        with open(sql_path, 'r', encoding='utf-8') as f:
            self.insert_query = f.read()

        # store 2 seasons crops
        self.crop_map = {}
    
    def process_item(self, item):
        name = item['name']
        season = item['season']

        try:
            base_price = float(item.get('sell_prices', 0))
        except (ValueError, TypeError):
            base_price = 0

        # calculate price by grades
        price_dict = {
            "Base": int(base_price * 1),
            "Bronze": int(round(base_price * 1.15)),
            "Silver": int(round(base_price * 1.30)),
            "Gold": int(round(base_price * 1.50)),
            "Osmium": int(round(base_price * 2.00))
        }
        
        # GROWTH TIME adn REGROWTH TIME to Number
        raw_days = item.get('growth_time', '0')
        raw_regrowth_days = item.get('re_growth_time', '0')
        # keep digit
        clean_days = ''.join(filter(str.isdigit, str(raw_days))) 
        clean_regrowth_days = ''.join(filter(str.isdigit, str(raw_regrowth_days))) 
        growth_int = int(clean_days) if clean_days else 0
        regrowth_int = int(clean_regrowth_days) if clean_regrowth_days else 0
        seed_price = int(item.get('seed_price'))

        if name in self.crop_map:
            if season not in self.crop_map[name]['seasons']:
                self.crop_map[name]['seasons'].append(season)
        else:
            crop_dict = dict(item)
            crop_dict['seasons'] = [season]
            crop_dict['sell_prices'] = price_dict                  
            crop_dict['growth_time'] = growth_int
            crop_dict['re_growth_time'] = regrowth_int
            crop_dict['seed_price'] = seed_price
            
            # Clean up unwanted fields
            if 'season' in crop_dict: del crop_dict['season'] 
            if 'sell_price_base' in crop_dict: del crop_dict['sell_price_base']
            # if 'seed_price' in crop_dict: del crop_dict['seed_price'] 
            
            self.crop_map[name] = crop_dict
            
        return item

    def close_spider(self):
        for data in self.crop_map.values():
            prices = data['sell_prices']
            
            self.cur.execute(self.insert_query, (
                data['name'],
                data['seasons'],
                data.get('town_rank'),
                data.get('growth_time'),
                data.get('re_growth_time'),
                data.get('possible_max_harvest'),
                data.get('image_url'),
                data.get('seed_price'),
                prices['Base'],
                prices['Bronze'],
                prices['Silver'],
                prices['Gold'],
                prices['Osmium']
            ))

        self.connection.commit()
        self.cur.close()
        self.connection.close()
        print("Database Import Completed")



