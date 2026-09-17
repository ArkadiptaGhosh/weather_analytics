import requests

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 22.5726,
    "longitude": 88.3639,
    "current": [
        "temperature_2m",
        "relative_humidity_2m",
        "wind_speed_10m"
    ]
}

response = requests.get(
    url,
    params=params,
    timeout=30
)

response.raise_for_status()

print(response.status_code)
print(response.json())


# Run this script to check API sample response by running below

# For Git Bash :- poetry run python src/weather_analytics/local_API_response_test/check_api.py

# For Terminal :-  poetry run python .\src\weather_analytics\local_API_response_test\check_api.py