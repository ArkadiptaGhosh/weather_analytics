import logging

from pyspark.sql import SparkSession

from weather_analytics.api.weather_client import WeatherClient
from weather_analytics.processing.bronze_processor import BronzeProcessor
from weather_analytics.config import (
    job_config,
    location
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main(config):
    """Bronze ingestion pipeline."""

    # Resolve the Bronze target table for the current environment.
    BRONZE_TABLE = job_config.get_bronze_table(config)

    logger.info("Starting weather data ingestion...")
    logger.info("------------------------------------------------------")

    # Reuse Databricks' active Spark session, or create one for local execution.
    spark = SparkSession.getActiveSession()

    if spark is None:
        spark = SparkSession.builder.getOrCreate()

    # Set up the API client and processor that adds Bronze audit metadata.
    client = WeatherClient()
    bronze_processor = BronzeProcessor()

    # Collect one raw API response for each configured location.
    bronze_records = []

    # Load the city coordinates used for weather API requests.
    all_locations = location.location_config()

    for city, latitude, longitude in all_locations:

        logger.info(
            f"Fetching weather data for {city}"
        )

        # A failed city request is logged and does not stop the full batch.
        try:
            weather = client.get_current_weather(
                city=city,
                latitude=latitude,
                longitude=longitude
            )
        except Exception as exc:
            logger.error(
                "Failed to fetch weather data for %s: %s",
                city,
                exc
            )
            continue

        # Preserve the raw API payload and add ingestion timestamp/source fields.
        bronze_data = bronze_processor.process(
            weather
        )

        bronze_records.append(
            bronze_data
        )


    logger.info("------------------------------------------------------")

    logger.info(
        f"Fetched weather data for {len(bronze_records)} cities"
    )

    # Avoid creating a schema-less DataFrame when every API request failed.
    if not bronze_records:
        logger.warning("No weather data was fetched; skipping Bronze write.")
        return

    # Convert the API payloads to a Spark DataFrame for the Delta write.
    bronze_df = spark.createDataFrame(
        bronze_records
    )

    # Append each ingestion batch to the raw, schema-flexible Bronze Delta table.
    bronze_df.write \
        .format("delta") \
        .mode("append") \
        .option("mergeSchema", "true") \
        .saveAsTable(
            BRONZE_TABLE
        )


    logger.info("------------------------------------------------------")

    logger.info(
        "Bronze data written to "
        f"{BRONZE_TABLE}"
    )


if __name__ == "__main__":
    main()
