"""
ETL Pipeline Orchestrator
"""

import logging
from pathlib import Path
import etl


# ──────────────────────────────
# Configuration
# ──────────────────────────────
log_path = "orchestrator.log"
input_file = "raw.json"


# ──────────────────────────────
# Set Up
# ──────────────────────────────
logging.basicConfig(
    filename=log_path,
    level=logging.DEBUG,
    format="%(asctime)s | %(name)s | %(levelname)-8s | %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


# ──────────────────────────────
# Main
# ──────────────────────────────
etl.main(input_file=Path(input_file))
