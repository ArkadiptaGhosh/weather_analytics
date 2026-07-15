import requests


class WeatherClient:
    """Client for communicating with the Weather API."""

    def __init__(self):
        """Initialize the Weather Client."""

        self.base_url = "https://api.open-meteo.com/v1/forecast"

    def get_current_weather(
        self,
        city: str,
        latitude: float,
        longitude: float
    ) -> dict:
        """Fetch the current weather for a location."""

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "wind_speed_10m"
            ]
        }

        response = requests.get(
            self.base_url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        if response.status_code == 200:
            weather_data = response.json()

            weather_data["city"] = city

            return weather_data

        raise Exception(
            f"Weather API request failed with status code {response.status_code}"
        )