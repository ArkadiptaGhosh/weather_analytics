class SilverProcessor:

    """Add ingesestion metadata to the weather data."""

    def process(self, weather_data: dict) -> dict:

        return {
            "latitude": weather_data.get("latitude"),
            "longitude": weather_data.get("longitude"),
            "temperature": (
                weather_data.get("current", {})
                           .get("temperature_2m")
            ),
            "weather_time": (
                weather_data.get("current", {})
                           .get("time")
            ),
            "timezone": weather_data.get("timezone"),
            "ingestion_timestamp": (
                weather_data.get("ingestion_timestamp")
            ),
            "source_system": (
                weather_data.get("source_system")
            )
        }