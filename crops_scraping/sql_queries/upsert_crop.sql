
            INSERT INTO crops (
                name, seasons, town_rank, growth_time, 
                possible_max_harvest, image_url,
                price_base, price_bronze, price_silver, price_gold, price_osmium
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (name) 
            DO UPDATE SET 
                seasons = EXCLUDED.seasons,
                town_rank = EXCLUDED.town_rank,
                growth_time = EXCLUDED.growth_time,
                possible_max_harvest = EXCLUDED.possible_max_harvest,
                image_url = EXCLUDED.image_url,
                price_base = EXCLUDED.price_base,
                price_bronze = EXCLUDED.price_bronze,
                price_silver = EXCLUDED.price_silver,
                price_gold = EXCLUDED.price_gold,
                price_osmium = EXCLUDED.price_osmium;
