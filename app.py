from data_fetcher import DataFetcher
from processor import IntelligenceProcessor
import folium
from folium.plugins import HeatMap

def run_project(city_name):
    # --- PHASE 1: EXTRACTION ---
    # We initialize our fetcher and grab cafes
    fetcher = DataFetcher(city_name)
    raw_data = fetcher.fetch_pois({"amenity": "cafe"})
    
    if raw_data is None:
        print("Expert Alert: No data to process. Exiting.")
        return

    # --- PHASE 2: INTELLIGENCE ---
    # We pass the raw data into our processor
    brain = IntelligenceProcessor(raw_data)
    
    # We create a 15x15 grid of the city to find the 'hotspots'
    # Increase grid_size for more detail (but it takes longer!)
    grid_results = brain.find_best_spots(grid_size=15)

    # --- PHASE 3: VISUALIZATION ---
    # 1. Create a base map centered at the average location of our cafes
    center_lat = raw_data['geometry'].y.mean()
    center_lon = raw_data['geometry'].x.mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=14, tiles="cartodbpositron")

    # 2. Add the HeatMap layer using our calculated scores
    # Folium's HeatMap expects a list of [lat, lon, weight]
    heat_data = [[row['lat'], row['lon'], row['score']] for index, row in grid_results.iterrows()]
    HeatMap(heat_data, radius=25, blur=15, min_opacity=0.5).add_to(m)

    # 3. Add individual markers for the actual cafes so we can compare
    for index, row in raw_data.iterrows():
        folium.CircleMarker(
            location=[row['geometry'].y, row['geometry'].x],
            radius=3,
            color='blue',
            fill=True,
            popup=row['name']
        ).add_to(m)

    # 4. Save the final result
    output_file = "urban_analysis.html"
    m.save(output_file)
    print(f"--- SUCCESS! ---")
    print(f"Intelligence report saved to {output_file}")

if __name__ == "__main__":
    # You can change this to any city! 
    # Try "Hoboken, New Jersey, USA" for a fast test.
    run_project("Munich, Bavaria, Germany")