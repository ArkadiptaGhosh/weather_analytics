CREATE TABLE IF NOT EXISTS weather_analytics.silver.weather_curated (
    city STRING,
    latitude DOUBLE,
    longitude DOUBLE,
    temperature DOUBLE,
    humidity INT,
    wind_speed DOUBLE,
    weather_time TIMESTAMP,
    timezone STRING,
    ingestion_timestamp TIMESTAMP,
    silver_processed_timestamp TIMESTAMP,
    ingestion_source STRING,
    elevation INTEGER,
    temperature_unit STRING,
    humidity_unit STRING,
    wind_speed_unit STRING
)
USING DELTA;