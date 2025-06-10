"""
A minimal CLI template that:
  • Accepts --input <file> and --log <file> flags (both required)
  • Appends a timestamp (YYYYMMDD_HHMMSS) to the log-file name
  • Configures DEBUG-level logging to that file
"""

from __future__ import annotations

import argparse
import logging
from datetime import datetime
from pathlib import Path


# ──────────────────────────────
# Set Up
# ──────────────────────────────
def parse_args() -> argparse.Namespace:
    """Return Namespace with input_file and log_file attributes."""
    parser = argparse.ArgumentParser(
        description="Demo CLI with timestamped log file."
    )

    parser.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Path to the input file to process.",
    )
    parser.add_argument(
        "--log",
        required=True,
        type=Path,
        help="Base path for the log file (timestamp is appended automatically).",
    )

    return parser.parse_args()

def timestamped_path(base_path: Path) -> Path:
    """
    Insert YYYYmmdd_HHMMSS before the file's extension.

    Examples
    --------
    /tmp/app.log  -> /tmp/app_20250610_071234.log
    logs/run.txt  -> logs/run_20250610_071234.txt
    """
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    if base_path.suffix:
        new_name = f"{base_path.stem}_{ts}{base_path.suffix}"
    else:
        new_name = f"{base_path.name}_{ts}"
    return base_path.with_name(new_name)

def configure_logging(log_path: Path) -> None:
    """
    Set root logger to DEBUG and write to log_path.

    Notes
    -----
    logging.debug    | Detailed, step-by-step diagnostic information for developers.
    logging.info     | High-level progress messages: start/finish of tasks, key results.
    logging.warning  | Something unexpected happened but the program can still proceed.
    logging.error    | A failure occurred; part of the task could not be completed.
    logging.critical | A fatal error—program (or a major subsystem) cannot continue safely.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(),  # also echo to stdout
        ],
    )
    logging.debug("Logging to %s", log_path.resolve())


# ──────────────────────────────
# Utilities
# ──────────────────────────────




# ──────────────────────────────
# Processes
# ──────────────────────────────




# ──────────────────────────────
# Main
# ──────────────────────────────
def main(*, input_file: Path) -> None:
    """
    Main workflow.

    Parameters
    ----------
    input_file : Path
        The file to process.
    """
    logging.debug("Starting processing on %s", input_file)

    if input_file.exists():
        pass
    else:
        logging.error("File not found: %s", input_file)
        return

    logging.debug("Finished processing")


# ──────────────────────────────
# Entry Point
# ──────────────────────────────
if __name__ == "__main__":
    # Set Up
    args = parse_args()
    full_log_path = timestamped_path(args.log)
    configure_logging(full_log_path)

    # Main
    main(input_file=args.input)
