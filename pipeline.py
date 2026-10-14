"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --config config.yaml --output clean.csv
    python pipeline.py --input data.csv --config config.yaml --output clean.csv --verbose
"""

import argparse
import logging
import sys

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)

logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Parses command-line arguments"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to the input file"
    )
    parser.add_argument(
        "--config", "-c",
        required=True,
        help="Path to the YAML configuration file"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Path to save the cleaned CSV file"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show debug-level log messages",
    )
    return parser.parse_args()


def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug(f"Arguments received: {args}")

    if not validate_input(args.input):
        sys.exit(1)
    if not validate_input(args.config):
        sys.exit(1)

    logger.info("Starting pipeline")

    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError as e:
        logger.error(f"Could not load the input or config file: {e}")
        sys.exit(1)

    logger.info(f"Loaded data from {args.input} and config from {args.config}")


    validation = config["validation"]
    required_columns = validation["required_columns"]
    numeric_columns = validation["numeric_columns"]

    rows_before_validation = len(data)
    try:
        data = validate_dataframe(data, required_columns, numeric_columns)
    except ValueError:
        sys.exit(1)

    logger.info(f"Validation complete: {rows_before_validation} -> {len(data)} rows")


    original_data = data.copy()

    try:
        data = process_data(data, config)
    except ValueError:

        sys.exit(1)


    report = create_cleaning_report(original_data, data)

    logger.info(
        f"Processing complete: {report['rows_before']} -> {report['rows_after']} rows, "
        f"removed {report['rows_removed']} row(s) and {report['columns_removed']} column(s)"
    )


    output_path = save_data(data, args.output)

    logger.info(f"Saved {len(data)} rows and {len(data.columns)} columns to {output_path}")


    print("Cleaning report:")
    for key, value in report.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()