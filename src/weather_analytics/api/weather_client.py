import requests


class WeatherClient:
    """Client for communicating with the Weather API."""

    def __init__(self):
        """Initialize the Weather Client."""

        self.base_url = "https://api.open-meteo.com/v1/forecast"

    def get_current_weather(self):
        """Fetch the current weather."""

        params = {
            "latitude": 22.57,
            "longitude": 88.36,
            "current": "temperature_2m"
        }

        response = requests.get(
            self.base_url,
            params=params
        )

        if response.status_code == 200:
            return response.json()

        raise Exception(
            f"Weather API request failed with status code {response.status_code}"
        )