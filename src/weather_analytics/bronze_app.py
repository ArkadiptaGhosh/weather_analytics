import logging

from pyspark.sql import SparkSession

from weather_analytics.api.weather_client import WeatherClient
from weather_analytics.processing.bronze_processor import BronzeProcessor
from weather_analytics.config.location import BRONZE_TABLE, LOCATIONS


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """Bronze ingestion pipeline."""

    logger.info("Starting weather data ingestion...")
    logger.info("------------------------------------------------------")

    spark = SparkSession.getActiveSession()

    if spark is None:
        spark = SparkSession.builder.getOrCreate()

    client = WeatherClient()
    bronze_processor = BronzeProcessor()

    bronze_records = []

    for city, latitude, longitude in LOCATIONS:

        logger.info(
            f"Fetching weather data for {city}"
        )

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

    if not bronze_records:
        logger.warning("No weather data was fetched; skipping Bronze write.")
        return

    bronze_df = spark.createDataFrame(
        bronze_records
    )

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