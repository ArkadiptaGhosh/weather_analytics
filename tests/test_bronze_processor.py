from datetime import datetime, timezone

from weather_analytics.processing.bronze_processor import BronzeProcessor


def test_process_adds_ingestion_metadata():
    weather_data = {
        "city": "Bangalore",
        "current": {
            "temperature_2m": 28.5,
            "relative_humidity_2m": 70,
            "wind_speed_10m": 12.3,
        },
    }

    processor = BronzeProcessor()

    result = processor.process(weather_data)

    assert "ingestion_timestamp" in result
    assert isinstance(result["ingestion_timestamp"], datetime)
    assert result["ingestion_timestamp"].tzinfo == timezone.utc

    assert "ingestion_source" in result
    assert result["ingestion_source"] == "Open Weather API"

    assert result["city"] == "Bangalore"