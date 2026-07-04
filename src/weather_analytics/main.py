from datetime import datetime
from pathlib import Path

from weather_analytics.api.weather_client import WeatherClient
from weather_analytics.config.config import BRONZE_DIRECTORY
from weather_analytics.storage.file_manager import FileManager


def main():
    """Application entry point."""

    client = WeatherClient()
    file_manager = FileManager()

    weather = client.get_current_weather()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = f"weather_{timestamp}.json"

    file_path = Path(BRONZE_DIRECTORY) / file_name

    file_manager.save_json(weather, str(file_path))


if __name__ == "__main__":
    main()