import time

import requests


class WeatherClient:
    """Client for retrieving current weather data from the Open-Meteo API.

    The client manages the base API URL, retry configuration, and the request
    flow used to fetch weather snapshots for a given city and coordinate pair.
    """

    def __init__(self):
        """Initialize the weather client configuration.

        Sets the request endpoint and retry/backoff values used when fetching
        weather data from the external API.
        """

        self.base_url = "https://api.open-meteo.com/v1/forecast"

        self.max_attempts = 3
        self.initial_backoff = 1  # seconds

    def get_current_weather(
        self,
        city: str,
        latitude: float,
        longitude: float
    ) -> dict:
        """Fetch the current weather for the provided location.

        Args:
            city: Human-readable city name to associate with the returned data.
            latitude: Latitude of the location in decimal degrees.
            longitude: Longitude of the location in decimal degrees.

        Returns:
            A dictionary containing the weather response payload from the API,
            including the city name.

        Raises:
            requests.exceptions.Timeout: If the request times out after all retry
                attempts.
            requests.exceptions.ConnectionError: If the connection fails after
                all retry attempts.
            requests.exceptions.HTTPError: If the API returns a non-retryable
                HTTP error status.
        """

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "wind_speed_10m"
            ]
        }

        for attempt in range(self.max_attempts):
            try:
                response = requests.get(
                    self.base_url,
                    params=params,
                    timeout=30
                )

                response.raise_for_status()

                weather_data = response.json()
                weather_data["city"] = city

                return weather_data

            except requests.exceptions.HTTPError as exc:
                status_code = (
                    exc.response.status_code
                    if exc.response is not None
                    else None
                )

                retryable_status_codes = {500, 502, 503, 504}

                if status_code not in retryable_status_codes:
                    raise

                if attempt == self.max_attempts - 1:
                    raise

                time.sleep(
                    self.initial_backoff * (2 ** attempt)
                )

            except (
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError
            ):
                if attempt == self.max_attempts - 1:
                    raise

                time.sleep(
                    self.initial_backoff * (2 ** attempt)
                )