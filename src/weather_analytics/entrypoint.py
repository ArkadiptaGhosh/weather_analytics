import argparse


import weather_analytics.bronze_app as BronzeRun
import weather_analytics.silver_app as SilverRun


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
parser.add_argument("--env", required=False, help="Specify the environment (dev or prod)")
parser.add_argument("--email_id", required=True, help="Specify the email ID for notifications")

args = parser.parse_args()

def main():
    if args.layer == "bronze":
        BronzeRun.main(args)
    elif args.layer == "silver":
        SilverRun.main(args)
    else:
        raise ValueError("Invalid layer specified. Use 'bronze' or 'silver'.")


if __name__ == "__main__":
    main()

