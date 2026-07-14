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

    # Fetch weather data from API
    weather = client.get_current_weather()

    # Add ingestion metadata
    bronze_data = bronze_processor.process(weather)

    # ---------------------------------------------------------
    # Temporary local JSON backup
    # ---------------------------------------------------------

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = f"weather_{timestamp}.json"

    file_path_bronze = Path(BRONZE_DIRECTORY) / file_name

    file_manager.save_json(
        bronze_data,
        str(file_path_bronze)
    )

    print(f"Bronze JSON saved to {file_path_bronze}")

    # ---------------------------------------------------------
    # Write to Bronze Delta table
    # ---------------------------------------------------------

    bronze_df = spark.createDataFrame([bronze_data])

    bronze_df.write \
        .format("delta") \
        .mode("append") \
        .saveAsTable(
            "weather_analytics.bronze.weather_raw"
        )

    print(
        "Bronze data written to "
        "weather_analytics.bronze.weather_raw"
    )


if __name__ == "__main__":
    main()