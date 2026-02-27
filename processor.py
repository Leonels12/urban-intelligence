import pandas as pd
import numpy as np

class IntelligenceProcessor:
    def __init__(self, poi_dataframe):
        """
        Takes the mined data (the DataFrame from our Fetcher)
        and prepares it for analysis.
        """
        self.df = poi_dataframe

    def calculate_score(self, target_lat, target_lon, radius_km=1.0):
        """
        This is the "Brain." It calculates a score for a specific spot 
        based on how many POIs are within the 'radius_km'.
        """
        total_score = 0
        
        # We loop through every cafe we found
        for index, row in self.df.iterrows():
            # Get the coordinates of the cafe
            # (Note: OSMnx points are stored as POINT(lon lat))
            poi_lon = row['geometry'].x
            poi_lat = row['geometry'].y
            
            # 1. Calculate a simple Euclidean distance
            # (Expert note: In a real global app, we'd use the Haversine formula, 
            # but for a city-level project, this is faster and works well!)
            dist = np.sqrt((target_lat - poi_lat)**2 + (target_lon - poi_lon)**2)
            
            # Convert degrees-ish to kilometers (roughly 111km per degree)
            dist_km = dist * 111
            
            # 2. Distance Decay Logic:
            # If the cafe is within our radius, add to the score.
            # Closer cafes give a much higher score.
            if dist_km <= radius_km:
                # Formula: 1 / (distance + small_buffer)
                # This ensures we don't divide by zero and creates a nice curve.
                total_score += 1 / (dist_km + 0.1)
                
        return round(total_score, 2)

    def find_best_spots(self, grid_size=10):
        """
        This is the 'Mining' part. It creates a grid over the city 
        and finds the hottest 'Intelligence' spots.
        """
        # Get the boundaries of our data
        min_lon, min_lat, max_lon, max_lat = self.df.total_bounds
        
        print(f"Analyzing area from {min_lat} to {max_lat}...")
        
        # Create a grid of points to check
        lat_samples = np.linspace(min_lat, max_lat, grid_size)
        lon_samples = np.linspace(min_lon, max_lon, grid_size)
        
        results = []
        for lat in lat_samples:
            for lon in lon_samples:
                score = self.calculate_score(lat, lon)
                results.append({'lat': lat, 'lon': lon, 'score': score})
        
        return pd.DataFrame(results)