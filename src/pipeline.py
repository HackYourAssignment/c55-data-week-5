"""
Week 5 assignment: containerised data pipeline.
"""

import logging
import os
from pathlib import Path

from src.clean import clean_sales, load_and_explore
from src.ingest import download_inputs, upload_outputs
from src.report import build_reports, write_outputs
from src.transform import join_customers

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def get_config() -> dict:
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise RuntimeError("API_KEY environment variable is required")

    return {
        "api_key": api_key,
        "data_dir": os.getenv("DATA_DIR", "data"),
        "output_dir": os.getenv("OUTPUT_DIR", "output"),
        "upload_to_azure": os.getenv("UPLOAD_TO_AZURE", "false").lower() == "true",
    }


def run() -> None:
    config = get_config()

    data_dir = Path(config["data_dir"])
    output_dir = Path(config["output_dir"])

    logger.info("Starting Week 5 containerised pipeline")
    use_azure = os.getenv("USE_AZURE", "false").lower() == "true"
    if use_azure:
        download_inputs(data_dir)
    else:
        logger.info("Using local data directory: %s", data_dir)
    
    sales_raw, customers_raw = load_and_explore(data_dir)
    sales_clean = clean_sales(sales_raw)
    enriched = join_customers(sales_clean, customers_raw)

    reports = build_reports(enriched)
    write_outputs(reports, output_dir)

    if config["upload_to_azure"]:
        upload_outputs(output_dir, config["api_key"])

    logger.info("Pipeline complete")


if __name__ == "__main__":
    run()
