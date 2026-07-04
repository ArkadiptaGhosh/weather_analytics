from weather_analytics.api.weather_client import WeatherClient
from weather_analytics.storage.file_manager import FileManager
from weather_analytics.config.config import BRONZE_FILE_PATH


def main():
    """Application entry point."""

    client = WeatherClient()
    file_manager = FileManager()

    weather = client.get_current_weather()

    file_manager.save_json(weather, BRONZE_FILE_PATH)


if __name__ == "__main__":
    main()