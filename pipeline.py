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
from pathlib import Path

from data_loaders import load_data
from data_processor import process_data, create_cleaning_report

logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
        datefmt="%H:%M:%S",
    )


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


def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    path = Path(filepath)
    if not path.exists():
        logger.error(f"Input path does not exist: {path}")
        return False
    if not path.is_file():
        logger.error(f"Input path is not a file: {path}")
        return False
    logger.info(f"Input file found: {path.name}")
    return True


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


    original_data = data.copy()

    try:
        data = process_data(data, config)
    except ValueError:

        sys.exit(1)


    report = create_cleaning_report(original_data, data)
    print("Cleaning report:")
    for key, value in report.items():
        print(f"  {key}: {value}")


    logger.info(
        f"Processing complete: removed {report['rows_removed']} row(s) "
        f"and {report['columns_removed']} column(s)"
    )


    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path, index=False)


    logger.info(f"Saved {len(data)} rows and {len(data.columns)} columns to {output_path}")


if __name__ == "__main__":
    main()