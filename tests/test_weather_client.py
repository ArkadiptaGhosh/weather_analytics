# Import the Python standard library and the WeatherClient dependency.
from unittest.mock import patch

import pytest
import requests

from weather_analytics.api.weather_client import WeatherClient


# Test: verify the client transforms the API payload into the expected output.
@patch("weather_analytics.api.weather_client.requests.get")
def test_get_current_weather(mock_get):

    # Arrange: mock a successful API response for Kolkata weather data.
    mock_get.return_value.status_code = 200

    mock_get.return_value.json.return_value = {
        "latitude": 22.5726,
        "longitude": 88.3639,
        "current": {
            "temperature_2m": 28.5,
            "relative_humidity_2m": 70,
            "wind_speed_10m": 12.3
        }
    }

    client = WeatherClient()

    # Act: call the weather API wrapper with the city and coordinates.
    result = client.get_current_weather(
        city="Kolkata",
        latitude=22.5726,
        longitude=88.3639
    )

    # Assert: the client sends the expected endpoint, query parameters, and timeout.
    mock_get.assert_called_once_with(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": 22.5726,
            "longitude": 88.3639,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "wind_speed_10m"
            ]
        },
        timeout=30
    )

    assert result["city"] == "Kolkata"
    assert result["current"]["temperature_2m"] == 28.5
    assert result["current"]["relative_humidity_2m"] == 70
    assert result["current"]["wind_speed_10m"] == 12.3
    assert result["latitude"] == 22.5726
    assert result["longitude"] == 88.3639


# Test: verify the client raises an HTTPError when the API returns an HTTP error.
@patch("weather_analytics.api.weather_client.requests.get")
def test_get_current_weather_http_error(mock_get):

    # Arrange: make raise_for_status() simulate an HTTP 500 error.
    mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "500 Server Error"
    )

    client = WeatherClient()

    # Act + Assert:
    # The API call should raise an HTTPError because raise_for_status()
    # was configured to simulate an HTTP 500 response.
    with pytest.raises(requests.exceptions.HTTPError):
        client.get_current_weather(
            city="Kolkata",
            latitude=22.5726,
            longitude=88.3639
        )




@patch("weather_analytics.api.weather_client.requests.get")
def test_get_current_weather_connection_error(mock_get):

    # Arrange: simulate a connection failure while calling the Weather API.
    mock_get.side_effect = requests.exceptions.ConnectionError(
        "Unable to connect to Weather API"
    )

    client = WeatherClient()

    # Act + Assert:
    # The API call should raise a ConnectionError because the mock
    # was configured to simulate a connection failure.
    with pytest.raises(requests.exceptions.ConnectionError):
        client.get_current_weather(
            city="Kolkata",
            latitude=22.5726,
            longitude=88.3639
        )