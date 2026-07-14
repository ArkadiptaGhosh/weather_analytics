from datetime import datetime
from pathlib import Path

from pyspark.sql import SparkSession

from weather_analytics.api.weather_client import WeatherClient
from weather_analytics.config.config import BRONZE_DIRECTORY
from weather_analytics.storage.file_manager import FileManager
from weather_analytics.processing.bronze_processor import BronzeProcessor


def main():
    """Bronze ingestion pipeline."""

    print("Starting weather data ingestion...")

    spark = SparkSession.getActiveSession()

    if spark is None:
        spark = SparkSession.builder.getOrCreate()

    client = WeatherClient()
    file_manager = FileManager()
    bronze_processor = BronzeProcessor()

    locations = [
        ("Kolkata", 22.57, 88.36),
        ("Bangalore", 12.97, 77.59)
    ]

    bronze_records = []

    for city, latitude, longitude in locations:

        print(f"Fetching weather data for {city}")

        weather = client.get_current_weather(
            city=city,
            latitude=latitude,
            longitude=longitude
        )

        bronze_data = bronze_processor.process(weather)

        bronze_records.append(bronze_data)

    # ---------------------------------------------------------
    # Write to Bronze Delta table
    # ---------------------------------------------------------

    bronze_df = spark.createDataFrame(bronze_records)

    bronze_df.write \
        .format("delta") \
        .mode("append") \
        .option("mergeSchema", "true") \
        .saveAsTable(
            "weather_analytics.bronze.weather_raw"
        )

    print(
        "Bronze data written to "
        "weather_analytics.bronze.weather_raw"
    )


if __name__ == "__main__":
    main()