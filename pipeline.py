"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv
    python pipeline.py --input data.csv --output results.json --format json --verbose
"""

import argparse
import logging
import sys
from pathlib import Path


logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure logging for the pipeline."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%H:%M:%S",
    )
    pass  # TODO: implement


def parse_arguments():
    """Parse command-line arguments."""
    pass  # TODO: implement

    parser = argparse.ArgumentParser(
        description="Parses command-line arguments"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help = "Path to the input file"
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

    logger.info("Starting pipeline")
    # the rest of your pipeline steps go here


if __name__ == "__main__":
    main()