
            INSERT INTO crops (
                name, seasons, town_rank, growth_time_day, re_growth_time_day, 
                possible_max_harvest_day, image_url, seed_price,
                price_base, price_bronze, price_silver, price_gold, price_osmium
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (name) 
            DO UPDATE SET 
                seasons = EXCLUDED.seasons,
                town_rank = EXCLUDED.town_rank,
                growth_time_day = EXCLUDED.growth_time_day,
                re_growth_time_day = EXCLUDED.re_growth_time_day,
                possible_max_harvest_day = EXCLUDED.possible_max_harvest_day,
                image_url = EXCLUDED.image_url,
                seed_price = EXCLUDED.seed_price,
                price_base = EXCLUDED.price_base,
                price_bronze = EXCLUDED.price_bronze,
                price_silver = EXCLUDED.price_silver,
                price_gold = EXCLUDED.price_gold,
                price_osmium = EXCLUDED.price_osmium;
