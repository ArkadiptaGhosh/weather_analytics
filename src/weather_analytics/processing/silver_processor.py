from datetime import datetime, timezone
from pyspark.sql import functions as F


class SilverProcessor:
    def process(self,bronze_df):
        """Transform bronze weather record into silver record."""

        return bronze_df.select(
            F.col("city"),
            
            F.col("latitude").cast("double").alias("latitude"),
            
            F.col("longitude").cast("double").alias("longitude"),

            
            F.col("elevation").cast("int").alias("elevation"),
            
            F.col("current.temperature_2m").cast("double").alias("temperature"),

            F.col("current_units.temperature_2m").alias("temperature_unit"),
            
            F.col("current.relative_humidity_2m").cast("int").alias("humidity"),

            F.col("current_units.relative_humidity_2m").alias("humidity_unit"),
            
            F.col("current.wind_speed_10m").cast("double").alias("wind_speed"),

            F.col("current_units.wind_speed_10m").alias("wind_speed_unit"),
            
            F.to_timestamp(F.col("current.time")).alias("weather_time"),
            
            F.col("timezone"),
            
            F.col("ingestion_timestamp").cast("timestamp").alias("ingestion_timestamp"),
            
            F.col("ingestion_source"),
            
            F.current_timestamp().alias("silver_processed_timestamp")
        )