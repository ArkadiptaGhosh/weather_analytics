import argparse

import weather_analytics.bronze_app as BronzeRun
import weather_analytics.silver_app as SilverRun


parser = argparse.ArgumentParser(description="Weather Analytics")

parser.add_argument("--layer",required=True,help="Specify the layer to run: bronze or silver")

args = parser.parse_args()


def main():
    if args.layer == "bronze":
        BronzeRun.main()
    elif args.layer == "silver":
        SilverRun.main()
    else:
        raise ValueError("Invalid layer specified. Use 'bronze' or 'silver'.")


if __name__ == "__main__":
    main()

