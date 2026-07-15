import logging

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from weather_analytics.config.location import (
    BRONZE_TABLE,
    SILVER_TABLE
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main():
    """Silver transformation pipeline."""

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

    silver_df = new_bronze_df.select(
        "city",

        F.col(
            "latitude"
        ).cast(
            "double"
        ).alias(
            "latitude"
        ),

        F.col(
            "longitude"
        ).cast(
            "double"
        ).alias(
            "longitude"
        ),

        F.col(
            "current"
        )[
            "temperature_2m"
        ].cast(
            "double"
        ).alias(
            "temperature"
        ),

        F.col(
            "current"
        )[
            "relative_humidity_2m"
        ].cast(
            "int"
        ).alias(
            "humidity"
        ),

        F.col(
            "current"
        )[
            "wind_speed_10m"
        ].cast(
            "double"
        ).alias(
            "wind_speed"
        ),

        F.to_timestamp(
            F.col(
                "current"
            )[
                "time"
            ]
        ).alias(
            "weather_time"
        ),

        "timezone",

        F.col(
            "ingestion_timestamp"
        ).cast(
            "timestamp"
        ).alias(
            "ingestion_timestamp"
        ),

        F.current_timestamp().alias(
            "silver_processed_timestamp"
        ),

        "ingestion_source"
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


if __name__ == "__main__":
    main()