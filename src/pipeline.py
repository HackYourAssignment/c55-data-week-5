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

from src.ingest import download_inputs, upload_outputs
from src.clean import load_and_explore, clean_sales
from src.transform import join_customers
from src.report import build_reports, write_outputs

_ROOT = Path(__file__).resolve().parent.parent
_env_file = _ROOT / ".env"
if _env_file.is_file():
    from dotenv import load_dotenv

    load_dotenv(_env_file)

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = Path("data")
DEFAULT_OUTPUT_DIR = "output"


def get_config() -> dict:
    """
    Return configuration read from environment variables.

    Required variables: API_KEY, GITHUB_USERNAME
    Optional variable: OUTPUT_DIR (default "output")

    Raise RuntimeError with a clear message if a required variable is missing.
    """
    api_key = os.environ.get("API_KEY")
    if not api_key:
        raise RuntimeError("API_KEY environment variable is required but not set")
    github_username = os.environ.get("GITHUB_USERNAME")
    if not github_username:
        raise RuntimeError(
            "GITHUB_USERNAME environment variable is required but not set"
        )
    output_dir = os.environ.get("OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    return {
        "api_key": api_key,
        "output_dir": output_dir,
        "github_username": github_username,
    }


def fetch_data(api_key: str) -> list[dict]:
    """
    Simulate fetching records from an external API.

    Return a list of at least one dict representing a record.
    In a real pipeline you would call requests.get(...) here.
    """
    _ = api_key  # reserved for a real HTTP client
    return [{"id": 1, "source": "api", "status": "ok"}]


def save_results(records: list[dict], output_dir: Path) -> None:
    """
    Write each record as a line to output_dir/results.txt.

    Create output_dir if it does not exist.
    Log the number of records written.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    results_file = output_dir / "results.txt"
    with results_file.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(f"{record}\n")
    logger.info("wrote %d records to %s", len(records), results_file)


def run() -> None:
    config = get_config()
    logger.info("starting pipeline")
    records = fetch_data(config["api_key"])
    output_dir = Path(config["output_dir"])
    save_results(records, output_dir)
    logger.info("pipeline complete")
    download_inputs(DATA_DIR)

    sales_raw, customers_raw = load_and_explore(DATA_DIR)

    sales_clean = clean_sales(sales_raw)
    enriched = join_customers(sales_clean, customers_raw)

    reports = build_reports(enriched)
    write_outputs(reports, output_dir)

    upload_outputs(output_dir, config["github_username"])

    logging.info("Pipeline complete.")


if __name__ == "__main__":
    run()
