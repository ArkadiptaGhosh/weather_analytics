import requests


class WeatherClient:
    "Client for communicating with the Weather API."
    def __int__(self):
         """Initialize the Weather API client."""

         self.base_url = "https://api.open-meteo.com/v1/forecast"
         self.timeout = 30
    def get_current_weather(self):

        params = {
            "latitude" : 22.57,
            "longitude":88.36,
            "current": "temperature_2m"
        }
         
        """Retrieve the current weather.""" 
        response = requests.Response(self.base_url,
                                     params = params)
        
        if requests.status_codes == 200 :
            return response.json()