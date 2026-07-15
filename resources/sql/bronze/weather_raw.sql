CREATE TABLE IF NOT EXISTS weather_analytics.bronze.weather_raw (
    city STRING,
    current MAP<STRING, STRING>,
    current_units MAP<STRING, STRING>,
    elevation DOUBLE,
    generationtime_ms DOUBLE,
    ingestion_source STRING,
    ingestion_timestamp TIMESTAMP, -- Changed from STRING to TIMESTAMP for best practice
    latitude DOUBLE,
    longitude DOUBLE,
    timezone STRING,
    timezone_abbreviation STRING,
    utc_offset_seconds BIGINT
)
USING DELTA;