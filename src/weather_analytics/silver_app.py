import logging

from pyspark.sql import SparkSession

from weather_analytics.config import location
from weather_analytics.processing.silver_processor import SilverProcessor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main(args):
    """Silver transformation pipeline."""
    BRONZE_TABLE = location.get_bronze_table(args)
    SILVER_TABLE = location.get_silver_table(args)
    run_id = args.run_id if args.run_id else " "
    execution_date = args.execution_date if args.execution_date else " "
    env = args.env if args.env else " "

    logger.info("Starting silver pipeline...")
    logger.info(
        "------------------------------------------------------"
    )

    spark = SparkSession.getActiveSession()

    if spark is None:
        spark = SparkSession.builder.getOrCreate()

    # ---------------------------------------------------------
    # Read Bronze table
    # ---------------------------------------------------------

    bronze_df = spark.read.table(
        BRONZE_TABLE
    )

    logger.info(
        f"Bronze records available: "
        f"{bronze_df.count()}"
    )

    # ---------------------------------------------------------
    # Read already processed Silver keys
    # ---------------------------------------------------------

    silver_keys_df = spark.read.table(
        SILVER_TABLE
    ).select(
        "city",
        "ingestion_timestamp"
    )

    # ---------------------------------------------------------
    # Incremental load
    # Get only records not already processed
    # ---------------------------------------------------------

    new_bronze_df = bronze_df.join(
        silver_keys_df,
        on=[
            "city",
            "ingestion_timestamp"
        ],
        how="left_anti"
    )

    logger.info(
        f"New Bronze records to process: "
        f"{new_bronze_df.count()}"
    )

    # ---------------------------------------------------------
    # Flatten Bronze JSON structure
    # ---------------------------------------------------------
    silver_processor = SilverProcessor()
   
    silver_df = silver_processor.process(
        new_bronze_df
    )

    # ---------------------------------------------------------
    # Write to Silver table
    # ---------------------------------------------------------

    silver_df.write \
        .format("delta") \
        .mode("append") \
        .option(
            "mergeSchema",
            "true"
        ) \
        .saveAsTable(
            SILVER_TABLE
        )

    logger.info(
        f"Silver data written successfully to "
        f"{SILVER_TABLE}"
    )

    if env == "prod":
        email_address = args.email_id if args.email_id else " "
        logger.info("------------------------------------------------------")
        logger.info(
            f"Weather analytics pipeline completed successfully for {email_address}!"
            f"for {run_id} and job started at {execution_date}"
        )


if __name__ == "__main__":
    main()