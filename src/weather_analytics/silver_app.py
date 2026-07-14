from datetime import datetime
from pathlib import Path

from weather_analytics.api.weather_client import WeatherClient
from weather_analytics.config.config import BRONZE_DIRECTORY
from weather_analytics.config.config import SILVER_DIRECTORY
from weather_analytics.storage.file_manager import FileManager
from weather_analytics.processing.bronze_processor import BronzeProcessor

def main():
    """Application entry point."""

    print("Silver pipeline started")    

    # client = WeatherClient()
    # file_manager = FileManager()

    # weather = client.get_current_weather()

    # bronze_processor = BronzeProcessor()
    # silver_processor = SilverProcessor()

    # bronze_data = bronze_processor.process(weather)
    # silver_data = silver_processor.process(bronze_data)

    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # file_name = f"weather_{timestamp}.json"

    # file_path_bronze = Path(BRONZE_DIRECTORY) / file_name
    # file_path_silver = Path(SILVER_DIRECTORY) / file_name

    # file_manager.save_json(bronze_data, str(file_path_bronze))
    # file_manager.save_json(silver_data, str(file_path_silver))

    # print(f"Weather data saved to {file_path_bronze} and {file_path_silver}")


if __name__ == "__main__":
    main()