import logging

from pyspark.sql import SparkSession

from weather_analytics.processing.silver_processor import (
    SilverProcessor
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)



def main():
    """Silver transformation pipeline."""

    logger.info("Starting silver pipeline...")
    logger.info("------------------------------------------------------")

    spark = SparkSession.getActiveSession()

    if spark is None:
        spark = SparkSession.builder.getOrCreate()

    silver_processor = SilverProcessor()

    bronze_df = spark.read.table(
        "weather_analytics.bronze.weather_raw"
    )

    bronze_rows = bronze_df.collect()

    silver_records = []

    for row in bronze_rows:

        silver_record = silver_processor.process(
            row.asDict(
                recursive=True
            )
        )

        silver_records.append(
            silver_record
        )

    silver_df = spark.createDataFrame(
        silver_records
    )

    silver_df.write \
        .format("delta") \
        .mode("append") \
        .option(
            "mergeSchema",
            "true"
        ) \
        .saveAsTable(
            "weather_analytics.silver.weather_curated"
        )

    logger.info(
        "Silver data written to "
        "weather_analytics.silver.weather_curated"
    )


if __name__ == "__main__":
    main()