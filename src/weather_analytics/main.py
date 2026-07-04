from weather_analytics.api.weather_client import WeatherClient


def main():

    """Apllication entry point."""
    client = WeatherClient()
    weather = client.get_current_weather()
    print(weather)



if __name__ == "__main__":
    main()