CREATE TABLE IF NOT EXISTS ${catalog}.${gold_schema}.${gold_table} (
    city STRING,
    weather_date DATE,
    avg_temperature DOUBLE,
    max_temperature DOUBLE,
    min_temperature DOUBLE,
    avg_humidity DOUBLE,
    avg_wind_speed DOUBLE,
    gold_processed_timestamp TIMESTAMP
)
USING DELTA;