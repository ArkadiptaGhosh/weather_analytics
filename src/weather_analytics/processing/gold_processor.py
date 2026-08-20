from pyspark.sql import functions as F


class GoldProcessor:

    def process(self, silver_df):
        """Create daily city-level weather summary."""

        return (
            silver_df
            .withColumn(
                "weather_date",
                F.to_date("weather_time")
            )
            .groupBy(
                "city",
                "weather_date"
            )
            .agg(
                F.avg("temperature").alias("avg_temperature"),
                F.max("temperature").alias("max_temperature"),
                F.min("temperature").alias("min_temperature"),
                F.avg("humidity").alias("avg_humidity"),
                F.avg("wind_speed").alias("avg_wind_speed"),
                F.count("*").alias("observation_count")
            )
            .withColumn(
                "gold_processed_timestamp",
                F.current_timestamp()
            )
        )