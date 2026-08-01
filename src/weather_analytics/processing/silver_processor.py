from datetime import datetime, timezone
from pyspark.sql import functions as F


class SilverProcessor:
    def process(self,bronze_df):
        """Transform bronze weather record into silver record."""

        return bronze_df.select(
            F.col("city"),
            
            F.col("latitude").cast("double").alias("latitude"),
            
            F.col("longitude").cast("double").alias("longitude"),
            
            F.col("current.temperature_2m").cast("double").alias("temperature"),
            
            F.col("current.relative_humidity_2m").cast("int").alias("humidity"),
            
            F.col("current.wind_speed_10m").cast("double").alias("wind_speed"),
            
            F.to_timestamp(F.col("current.time")).alias("weather_time"),
            
            F.col("timezone"),
            
            F.col("ingestion_timestamp").cast("timestamp").alias("ingestion_timestamp"),
            
            F.col("ingestion_source"),
            
            F.current_timestamp().alias("silver_processed_timestamp")
        )