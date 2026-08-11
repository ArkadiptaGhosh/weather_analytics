from dataclasses import dataclass

@dataclass
class JobConfig:
    """Job configuration dataclass."""

    layer: str

    bronze_catalogue: str | None = None
    bronze_schema: str | None = None
    bronze_table: str | None = None

    silver_catalogue: str | None = None
    silver_schema: str  | None = None
    silver_table: str | None = None


    gold_catalogue: str | None = None
    gold_schema: str | None = None
    gold_table: str | None = None

    run_id: str |  None = None
    execution_date: str | None = None



def get_bronze_table(config):
    return f"{config.bronze_catalogue}.{config.bronze_schema}.{config.bronze_table}"


def get_silver_table(config):
    return f"{config.silver_catalogue}.{config.silver_schema}.{config.silver_table}"