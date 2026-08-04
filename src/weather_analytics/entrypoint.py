import argparse

import logging


import weather_analytics.bronze_app as bronze_app
import weather_analytics.silver_app as silver_app

from weather_analytics.config.job_config import JobConfig


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_parser():


    parser = argparse.ArgumentParser(description="Weather Analytics")

    parser.add_argument("--layer",required=True,help="Specify the layer to run: bronze or silver")
    parser.add_argument("--bronze_catalogue", required=False, help="Specify the catalogue name")
    parser.add_argument("--bronze_schema", required=False, help="Specify the bronze schema name")
    parser.add_argument("--bronze_table", required=False, help="Specify the bronze table name")
    parser.add_argument("--silver_catalogue", required=False, help="Specify the silver catalogue name")
    parser.add_argument("--silver_schema", required=False, help="Specify the silver schema name")
    parser.add_argument("--silver_table", required=False, help="Specify the silver table name")
    parser.add_argument("--run_id", required=False, help="Specify the run ID")
    parser.add_argument("--execution_date", required=False, help="Specify the execution date")

    return parser


#######   Main Entrypoint of the weather_analytics Application   #######
def main():

    args = create_parser().parse_args()

    config = JobConfig(
        layer=args.layer,
        bronze_catalogue=args.bronze_catalogue,
        bronze_schema=args.bronze_schema,
        bronze_table=args.bronze_table,
        silver_catalogue=args.silver_catalogue,
        silver_schema=args.silver_schema,
        silver_table=args.silver_table,
        run_id=args.run_id,
        execution_date=args.execution_date
    )

    if config.layer == "bronze":
        logger.info("Running %s layer", config.layer)
        logger.info("------------------------------------------------------")
        logger.info("Bronze Catalogue: %s", config.bronze_catalogue)
        logger.info("Bronze Schema: %s", config.bronze_schema)
        logger.info("Bronze Table: %s", config.bronze_table)
        logger.info("------------------------------------------------------")
        logger.info("run_id: %s", config.run_id)
        logger.info("execution_date: %s", config.execution_date)

        # Running the Bronze Pipeline...
        bronze_app.main(config)

    elif config.layer == "silver":
        logger.info("------------------------------------------------------")
        logger.info("Silver Catalogue: %s", config.silver_catalogue)
        logger.info("Silver Schema: %s", config.silver_schema)
        logger.info("Silver Table: %s", config.silver_table)
        logger.info("Running %s layer", config.layer)
        logger.info("------------------------------------------------------")
        logger.info("run_id: %s", config.run_id)
        logger.info("execution_date: %s", config.execution_date)

        # Running the Silver Pipeline...
        silver_app.main(config)

    else:
        logger.error("Invalid layer specified: %s", config.layer)
        raise ValueError("Invalid layer specified")


if __name__ == "__main__":
    main()

