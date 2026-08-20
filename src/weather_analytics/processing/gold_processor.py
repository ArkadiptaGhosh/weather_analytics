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
                F.round(F.avg("temperature"), 2).alias("avg_temperature"),
                F.round(F.max("temperature"), 2).alias("max_temperature"),
                F.round(F.min("temperature"), 2).alias("min_temperature"),
                F.round(F.avg("humidity"), 2).alias("avg_humidity"),
                F.round(F.avg("wind_speed"), 2).alias("avg_wind_speed")
            )
            .withColumn(
                "gold_processed_timestamp",
                F.current_timestamp()
            )
        )