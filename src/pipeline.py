"""
Week 5 assignment: containerised data pipeline.

Tasks:
- Task 1: confirm this script runs locally before touching the Dockerfile.
- Task 5: read all configuration from environment variables (no hardcoded values).

Replace every `raise NotImplementedError` below with a real implementation.
"""

import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def get_config() -> dict:
    """
    Return configuration read from environment variables.

    Required variable: API_KEY
    Optional variable: OUTPUT_DIR (default "output")
    """
    api_key = os.getenv("API_KEY")

    if not api_key:
        raise RuntimeError("API_KEY is missing")

    output_dir = os.getenv("OUTPUT_DIR", "output")

    return {
        "api_key": api_key,
        "output_dir": output_dir,
    }


def fetch_data(api_key: str) -> list[dict]:
    """
    Simulate fetching records from an external API.
    """
    return [
        {"id": 1, "name": "Muna", "city": "Amsterdam"},
        {"id": 2, "name": "Ali", "city": "Rotterdam"},
    ]


def save_results(records: list[dict], output_dir: Path) -> None:
    """
    Write each record as a line to output_dir/results.txt
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / "results.txt"

    with open(file_path, "w", encoding="utf-8") as f:
        for record in records:
            f.write(f"{record}\n")

    logger.info("%s records written", len(records))


def run() -> None:
    config = get_config()
    logger.info("starting pipeline")

    records = fetch_data(config["api_key"])
    output_dir = Path(config["output_dir"])

    save_results(records, output_dir)

    logger.info("pipeline complete")


if __name__ == "__main__":
    run()