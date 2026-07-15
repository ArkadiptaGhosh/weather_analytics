from datetime import datetime, timezone

class BronzeProcessor:
    def process(self,weather_data:dict) -> dict:
        """Add ingesestion metadata to the weather data."""
        weather_data["ingestion_timestamp"] = datetime.now(timezone.utc)

        weather_data["ingestion_source"] = "Open Weather API"
        
        
        return weather_data