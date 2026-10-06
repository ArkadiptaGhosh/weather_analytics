# Import the Python standard library and the WeatherClient dependency.
from unittest.mock import patch, Mock

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
    mock_response = Mock()
    mock_response.status_code = 500

    http_error = requests.exceptions.HTTPError(
        "500 Server Error",
        response=mock_response
    )

    mock_get.return_value.raise_for_status.side_effect = http_error

    client = WeatherClient()

    # Act + Assert:
    # The API call should raise an HTTPError because raise_for_status()
    # was configured to simulate a 500 response.
    with pytest.raises(requests.exceptions.HTTPError):
        client.get_current_weather(
            city="Kolkata",
            latitude=22.5726,
            longitude=88.3639
        )


# Test: verify the client does not retry when the API returns HTTP 400.
@patch("weather_analytics.api.weather_client.time.sleep")
@patch("weather_analytics.api.weather_client.requests.get")
def test_get_current_weather_non_retryable_http_error(mock_get, mock_sleep):

    # Arrange: create a fake HTTP 400 response.
    mock_response = Mock()
    mock_response.status_code = 400

    http_error = requests.exceptions.HTTPError(
        "400 Bad Request",
        response=mock_response
    )

    # Configure raise_for_status() to raise the HTTP 400 error.
    mock_get.return_value.raise_for_status.side_effect = http_error

    client = WeatherClient()

    # Act + Assert:
    # The API call should immediately raise HTTPError.
    with pytest.raises(requests.exceptions.HTTPError):
        client.get_current_weather(
            city="Kolkata",
            latitude=22.5726,
            longitude=88.3639
        )

    # Assert: HTTP 400 is not retryable, so the API should be called only once.
    assert mock_get.call_count == 1

    # Assert: no retry delay should occur.
    mock_sleep.assert_not_called()


# Test: verify the client retries HTTP 500 errors and succeeds on a later attempt.
@patch("weather_analytics.api.weather_client.time.sleep")
@patch("weather_analytics.api.weather_client.requests.get")
def test_get_current_weather_http_retry_success(mock_get, mock_sleep):

    # Arrange: create fake HTTP 500 responses for the first two attempts.
    first_error_response = Mock()
    first_error_response.status_code = 500

    second_error_response = Mock()
    second_error_response.status_code = 500

    first_http_error = requests.exceptions.HTTPError(
        "500 Server Error",
        response=first_error_response
    )

    second_http_error = requests.exceptions.HTTPError(
        "500 Server Error",
        response=second_error_response
    )

    # Arrange: create a fake successful response for the third attempt.
    successful_response = Mock()
    successful_response.status_code = 200

    successful_response.json.return_value = {
        "latitude": 22.5726,
        "longitude": 88.3639,
        "current": {
            "temperature_2m": 28.5,
            "relative_humidity_2m": 70,
            "wind_speed_10m": 12.3
        }
    }

    # The first two API calls raise HTTP 500.
    # The third API call succeeds.
    mock_get.side_effect = [
        first_http_error,
        second_http_error,
        successful_response
    ]

    client = WeatherClient()

    # Act: call the weather API wrapper.
    result = client.get_current_weather(
        city="Kolkata",
        latitude=22.5726,
        longitude=88.3639
    )

    # Assert: the API was attempted three times.
    assert mock_get.call_count == 3

    # Assert: exponential backoff was used after the first
    # and second HTTP 500 errors.
    mock_sleep.assert_any_call(1)
    mock_sleep.assert_any_call(2)

    # Assert: the third attempt eventually returned the expected data.
    assert result["city"] == "Kolkata"
    assert result["current"]["temperature_2m"] == 28.5
    assert result["current"]["relative_humidity_2m"] == 70
    assert result["current"]["wind_speed_10m"] == 12.3
    assert result["latitude"] == 22.5726
    assert result["longitude"] == 88.3639


# Test: verify the client raises JSONDecodeError when the API response
# contains invalid JSON.
@patch("weather_analytics.api.weather_client.time.sleep")
@patch("weather_analytics.api.weather_client.requests.get")
def test_get_current_weather_invalid_json(mock_get, mock_sleep):

    # Arrange: create a fake response with an HTTP 200 status.
    mock_get.return_value.status_code = 200

    # Create an exception that simulates invalid JSON in the API response.
    json_error = requests.exceptions.JSONDecodeError(
        "Invalid JSON",
        "",
        0
    )

    # Configure response.json() to raise JSONDecodeError.
    mock_get.return_value.json.side_effect = json_error

    client = WeatherClient()

    # Act + Assert:
    # The API call should raise JSONDecodeError because the response
    # could not be decoded as valid JSON.
    with pytest.raises(requests.exceptions.JSONDecodeError):
        client.get_current_weather(
            city="Kolkata",
            latitude=22.5726,
            longitude=88.3639
        )

    # Assert: invalid JSON is not retryable, so the API should be
    # called only once.
    assert mock_get.call_count == 1

    # Assert: no retry delay should occur.
    mock_sleep.assert_not_called()


# Test: verify the client retries after timeouts and succeeds on a later attempt.
@patch("weather_analytics.api.weather_client.time.sleep")
@patch("weather_analytics.api.weather_client.requests.get")
def test_get_current_weather_timeout_retry_success(mock_get, mock_sleep):

    # Arrange: create a fake successful response for the third attempt.
    successful_response = mock_get.return_value

    successful_response.status_code = 200

    successful_response.json.return_value = {
        "latitude": 22.5726,
        "longitude": 88.3639,
        "current": {
            "temperature_2m": 28.5,
            "relative_humidity_2m": 70,
            "wind_speed_10m": 12.3
        }
    }

    # Make the first two API calls fail with Timeout,
    # and make the third API call return the successful response.
    mock_get.side_effect = [
        requests.exceptions.Timeout("Request timed out"),
        requests.exceptions.Timeout("Request timed out"),
        successful_response
    ]

    client = WeatherClient()

    # Act: call the weather API wrapper.
    result = client.get_current_weather(
        city="Kolkata",
        latitude=22.5726,
        longitude=88.3639
    )

    # Assert: the API was attempted three times.
    assert mock_get.call_count == 3

    # Assert: exponential backoff used 1 second after the first failure
    # and 2 seconds after the second failure.
    mock_sleep.assert_any_call(1)
    mock_sleep.assert_any_call(2)

    # Assert: the third attempt eventually returned the expected data.
    assert result["city"] == "Kolkata"
    assert result["current"]["temperature_2m"] == 28.5
    assert result["current"]["relative_humidity_2m"] == 70
    assert result["current"]["wind_speed_10m"] == 12.3
    assert result["latitude"] == 22.5726
    assert result["longitude"] == 88.3639


# Test: verify the client raises Timeout after all retry attempts fail.
@patch("weather_analytics.api.weather_client.time.sleep")
@patch("weather_analytics.api.weather_client.requests.get")
def test_get_current_weather_timeout_retry_exhausted(mock_get, mock_sleep):

    # Arrange: make every API call fail with a Timeout.
    mock_get.side_effect = requests.exceptions.Timeout(
        "Request timed out"
    )

    client = WeatherClient()

    # Act + Assert:
    # The API call should raise Timeout after all retry attempts are exhausted.
    with pytest.raises(requests.exceptions.Timeout):
        client.get_current_weather(
            city="Kolkata",
            latitude=22.5726,
            longitude=88.3639
        )

    # Assert: the API was attempted three times.
    assert mock_get.call_count == 3

    # Assert: exponential backoff used 1 second after the first failure
    # and 2 seconds after the second failure.
    mock_sleep.assert_any_call(1)
    mock_sleep.assert_any_call(2)


# Test: verify the client raises ConnectionError when the API cannot be reached.
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