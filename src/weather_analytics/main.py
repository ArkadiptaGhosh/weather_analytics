from weather_analytics.api.weather_client import WeatherClient
from weather_analytics.storage.file_manager import FileManager


def main():

    """Apllication entry point."""
    client = WeatherClient()
    weather = client.get_current_weather()
    FileManager.save_json(weather,"data/bronze/weather.json")


if __name__ == "__main__":
    main()