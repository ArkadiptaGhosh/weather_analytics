import logging

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from delta.tables import DeltaTable

from weather_analytics.config import job_config
from weather_analytics.processing.gold_processor import GoldProcessor


logger = logging.getLogger(__name__)


def main(config):
    """Gold analytics pipeline."""

    # Resolve the source and target table names for the current environment.
    SILVER_TABLE = job_config.get_silver_table(config)
    GOLD_TABLE = job_config.get_gold_table(config)

    logger.info("Starting Gold analytics...")
    logger.info("Gold target table: %s", GOLD_TABLE)

    # Reuse Databricks' active Spark session, or create one for local execution.
    spark = SparkSession.getActiveSession()

    if spark is None:
        spark = SparkSession.builder.getOrCreate()

    logger.info("Spark session available")

    # Read the cleaned weather observations from the Silver layer.
    silver_df = spark.read.table(SILVER_TABLE)

    # Find the newest observation date so Gold only refreshes that date's metrics.
    latest_weather_date = (
        silver_df
        .select(
            F.max(
                F.to_date("weather_time")
            ).alias("latest_weather_date")
        )
        .collect()[0]["latest_weather_date"]
    )

    # Keep only Silver records that contribute to the latest daily aggregates.
    affected_silver_df = silver_df.filter(
        F.to_date("weather_time") == latest_weather_date
    )

    logger.info(
        "Latest weather date in Silver: %s",
        latest_weather_date
    )

    # Aggregate city-level weather observations into Gold business metrics.
    gold_processor = GoldProcessor()

    gold_df = gold_processor.process(
        affected_silver_df
    )

    # Access the target Delta table to upsert daily city metrics.
    gold_table = DeltaTable.forName(
        spark,
        GOLD_TABLE
    )

    # Update existing city/date metrics and insert metrics for new city/date pairs.
    (
        gold_table.alias("target")
        .merge(
            gold_df.alias("source"),
            """
            target.city = source.city
            AND target.weather_date = source.weather_date
            """
        )
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute()
    )

    logger.info(
        "Gold data merged successfully into "
        f"{GOLD_TABLE}"
    )

    logger.info("Gold pipeline completed successfully")


if __name__ == "__main__":
    main()
