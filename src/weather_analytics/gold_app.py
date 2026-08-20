import logging

from pyspark.sql import SparkSession

from weather_analytics.config import job_config
from weather_analytics.processing.gold_processor import GoldProcessor

logger = logging.getLogger(__name__)


def main(config):
    """Gold analytics pipeline."""
    SILVER_TABLE = job_config.get_silver_table(config)
    GOLD_TABLE = job_config.get_gold_table(config)

    logger.info("Starting Gold analytics...")
    logger.info("Gold target table: %s", GOLD_TABLE)

    spark = SparkSession.getActiveSession()

    if spark is None:
        spark = SparkSession.builder.getOrCreate()

    logger.info("Spark session available")

    # Gold transformation will be added here.

    silver_df = spark.read.table(SILVER_TABLE)

    logger.info(
    "Silver records available: %s",
    silver_df.count()
    )

    gold_processor = GoldProcessor()  # Initialize the GoldProcessor class

    gold_df = gold_processor.process(silver_df)  # Call the process method

    # Write the gold_df to the Gold table
    gold_df.write\
        .format("delta")\
        .mode("overwrite")\
        .option("overwriteSchema", "true")\
        .saveAsTable(GOLD_TABLE)

    logger.info("Gold pipeline completed successfully")