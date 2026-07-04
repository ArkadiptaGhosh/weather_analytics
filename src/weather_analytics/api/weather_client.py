import requests


class WeatherClient:
    "Client for communicating with the Weather API."
    def __int__(self):
         """Initialize the Weather API client."""

         self.base_url = "https://api.open-meteo.com/v1/forecast"
         self.timeout = 30
    def get_current_weather(self):
         
        """Retrieve the current weather.""" 
        response = requests.Response(self.base_url)