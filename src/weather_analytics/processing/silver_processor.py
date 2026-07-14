from datetime import datetime, timezone


class SilverProcessor:
    def process(
        self,
        weather_data: dict
    ) -> dict:
        """Transform bronze weather record into silver record."""

        current = weather_data.get(
            "current",
            {}
        )

        return {
            "city": weather_data.get(
                "city"
            ),

            "latitude": float(
                weather_data.get(
                    "latitude"
                )
            ),

            "longitude": float(
                weather_data.get(
                    "longitude"
                )
            ),

            "temperature": float(
                current.get(
                    "temperature_2m"
                )
            ),

            "humidity": int(
                current.get(
                    "relative_humidity_2m"
                )
            ),

            "wind_speed": float(
                current.get(
                    "wind_speed_10m"
                )
            ),

            "weather_time": current.get(
                "time"
            ),

            "timezone": weather_data.get(
                "timezone"
            ),

            "ingestion_timestamp": weather_data.get(
                "ingestion_timestamp"
            ),

            "ingestion_source": weather_data.get(
                "ingestion_source"
            ),
            "silver_processed_timestamp": (
                datetime.now(
                timezone.utc).isoformat()
),
        }