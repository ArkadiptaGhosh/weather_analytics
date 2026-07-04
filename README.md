# Weather Analytics

A production-style Data Engineering project built using Python, Poetry, Git, GitHub, and Databricks.

This project demonstrates how to build an end-to-end weather analytics pipeline by ingesting data from a Weather API, transforming it through multiple data layers, and preparing it for analytics and reporting.

---

## Project Architecture

```text
                Weather API
                     │
                     ▼
          Python Application
                     │
                     ▼
          Raw JSON (Bronze Layer)
                     │
                     ▼
        Cleaned Data (Silver Layer)
                     │
                     ▼
     Business Metrics (Gold Layer)
                     │
                     ▼
              Parquet Files
                     │
                     ▼
               Databricks
                     │
                     ▼
              Delta Lake Tables
                     │
                     ▼
      GitHub Actions (CI/CD Pipeline)
```

---

## Technology Stack

- Python 3.13
- Poetry
- Git
- GitHub
- Databricks
- Delta Lake
- PySpark
- GitHub Actions

---

## Project Structure

```text
weather_analytics/
│
├── .venv/
├── src/
│   └── weather_analytics/
│       ├── api/
│       ├── config/
│       ├── models/
│       ├── utils/
│       └── __init__.py
│
├── tests/
├── pyproject.toml
├── poetry.lock
├── README.md
└── .gitignore
```

---

## Learning Goals

- Learn professional Python project structure
- Build an end-to-end ETL pipeline
- Consume REST APIs
- Transform and validate data
- Store data in Delta Lake
- Deploy using Databricks Asset Bundles
- Automate deployments using GitHub Actions