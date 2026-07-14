SELECT
    city,
    latitude,
    longitude,
    CAST(current['temperature_2m'] AS DOUBLE) AS temperature,
    CAST(current['relative_humidity_2m'] AS INT) AS humidity,
    CAST(current['wind_speed_10m'] AS DOUBLE) AS wind_speed,
    TO_TIMESTAMP(current['time']) AS weather_time,
    timezone,
    TO_TIMESTAMP(ingestion_timestamp) AS ingestion_timestamp,
    ingestion_source
FROM weather_analytics.bronze.weather_raw