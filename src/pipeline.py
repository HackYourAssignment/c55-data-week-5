"""
Week 5 assignment: containerised data pipeline.

Tasks:
- Task 1: confirm this script runs locally before touching the Dockerfile.
- Task 5: read all configuration from environment variables (no hardcoded values).

Replace every `raise NotImplementedError` below with a real implementation.
"""

import logging
from pathlib import Path
import os
import json

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def get_config() -> dict:
    """
    Return configuration read from environment variables.

    Required variable: API_KEY
    Optional variable: OUTPUT_DIR (default "output")

    Raise RuntimeError with a clear message if a required variable is missing.
    """
    api_key = os.getenv("API_KEY")
    output_dir = os.getenv("OUTPUT_DIR")

    if not api_key:
        raise RuntimeError("Missing required environment variable: API_KEY")

    if not output_dir:
        output_dir = "output"

    return {"api_key": api_key, "output_dir": output_dir}


def fetch_data(api_key: str) -> list[dict]:
    """
    Simulate fetching records from an external API.

    Return a list of at least one dict representing a record.
    In a real pipeline you would call requests.get(...) here.
    """
    if not api_key:
        raise RuntimeError("API key must not be empty")

    return [{"id": 1, "name": "Halyna", "status": "active"},
             {"id": 2, "name": "Alice", "status": "inactive"}]

def save_results(records: list[dict], output_dir: Path) -> None:
    """
    Write each record as a line to output_dir/results.txt.

    Create output_dir if it does not exist.
    Log the number of records written.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    results_file = output_dir / "results.txt"
    with open(results_file, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")

    logger.info("Written %s records to %s/results.txt", len(records), output_dir)


def run() -> None:
    """Run the data pipeline."""
    config = get_config()
    logger.info("starting pipeline")
    records = fetch_data(config["api_key"])
    output_dir = Path(config["output_dir"])
    save_results(records, output_dir)
    logger.info("pipeline complete")


if __name__ == "__main__":
    run()
