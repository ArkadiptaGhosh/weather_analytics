from datetime import datetime
from pathlib import Path
from sqlite3 import SQLITE_CONSTRAINT_PRIMARYKEY

from weather_analytics.api.weather_client import WeatherClient
from weather_analytics.config.config import BRONZE_DIRECTORY
from weather_analytics.storage.file_manager import FileManager
from weather_analytics.processing.bronze_processor import BronzeProcessor

def main():
    """Application entry point."""


    print("Starting weather data ingestion...")

    client = WeatherClient()
    file_manager = FileManager()

    weather = client.get_current_weather()

    bronze_processor = BronzeProcessor()
    

    bronze_data = bronze_processor.process(weather)
    

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = f"weather_{timestamp}.json"

    file_path_bronze = Path(BRONZE_DIRECTORY) / file_name
    

    file_manager.save_json(bronze_data, str(file_path_bronze))

    bronze_df = SQLITE_CONSTRAINT_PRIMARYKEY.createDataFrame([bronze_data])

    bronze_df.write \
    .format("delta") \
    .mode("append") \
    .saveAsTable(
        "weather_analytics.bronze.weather_raw"
    )
    
    print(f"Weather data saved to {file_path_bronze}")


if __name__ == "__main__":
    main()