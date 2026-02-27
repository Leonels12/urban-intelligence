import osmnx as ox
import pandas as pd

class DataFetcher:
    """
    A professional-grade tool to mine Points of Interest (POIs) 
    from OpenStreetMap for any city in the world.
    """
    
    def __init__(self, city_name):
        self.city_name = city_name
        # Professional practice: Cache data locally so we don't 
        # download the same map twice. This respects the API's servers.
        ox.settings.use_cache = True
        ox.settings.log_console = True

    def fetch_pois(self, tags):
        """
        Mine the map for specific features (like cafes, parks, or hospitals).
        'tags' is a dictionary like {'amenity': 'cafe'}.
        """
        print(f"--- Mining data for {self.city_name}: {tags} ---")
        
        try:
            # This is the "mining" command. 
            # It searches the city for anything matching our tags.
            gdf = ox.features_from_place(self.city_name, tags=tags)
            
            if gdf.empty:
                print("No data found for these tags.")
                return None

            # OSM sometimes gives us 'Polygons' (the shape of the building).
            # To do math later, we need a single 'Point' (the center of the building).
            gdf['geometry'] = gdf['geometry'].centroid
            
            # We only keep the Name and the Location (Geometry). 
            # Deleting extra data makes our program faster.
            return gdf[['name', 'geometry']]
            
        except Exception as e:
            print(f"Expert Alert: Failed to fetch data. Error: {e}")
            return None

# This block only runs if you play THIS file directly. 
# It's a great way to test your code!
if __name__ == "__main__":
    # Let's test it with a famous area
    test_city = "Hoboken, New Jersey, USA"
    fetcher = DataFetcher(test_city)
    
    # We are mining for 'amenities' categorized as 'cafe'
    cafes = fetcher.fetch_pois({"amenity": "cafe"})
    
    if cafes is not None:
        print(cafes.head()) # Show the first 5 cafes found