"""
CLI driven ETL pipeline
"""

from __future__ import annotations

import argparse
from datetime import datetime
from joblib import Parallel, delayed
import logging
import multiprocessing as mp
import pandas as pd
from pathlib import Path
import sys
from typing import Callable, Any


# ──────────────────────────────
# Configuration
# ──────────────────────────────



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
def load_csv(file_path: Path) -> pd.DataFrame:
    """
    Load csv file into pandas dataframe

    Notes
    -----
    https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html

    sep: str                                    # Column delimiter
    header: int | None                          # Row number to use as column names
    names: list[str] | None                     # Explicit column names
    index_col: int | str | list[int] | bool     # Column(s) to set as index
    usecols: list[int] | list[str] | None       # Subset of columns to read
    dtype: dict[str, str] | None                # Force dtypes by column name
    converters: dict[str, callable] | None      # Convert values in column during ingest
    true_values: list[str] | None               # Values to be considered True
    false_values: list[str] | None              # Values to be considered False
    skipinitialspace: bool                      # Skip spaces after delimiter
    parse_dates: list[int] | list[str] | bool   # Parse dates into datetime64
    date_format: str, dict[str, str]            # Format of dates to parse
    nrows: int | None                           # Read only first N rows
    skiprows: int | list[int] | None            # Skip specific rows at start
    skipfooter: int                             # Skip specific rows at end
    encoding: str | None                        # Character encoding
    na_values: list[str] | str | None           # Additional strings as NA/NaN
    thousands: str                              # Character to denote thousands separator
    decimal: str                                # Character to denote decimal point
    lineterminator: str                         # Character to denote a line break
    quotechar: str                              # Character to denote beginning and ending of a quoted item
    escapechar: str                             # Character used to escape other characters
    comment: str                                # Character used to indicate the rest of the line should not be parsed
    """
    logging.debug("Reading CSV: %s", file_path)
    try:
        df = pd.read_csv(
            file_path,
            sep=",",
            header=0,
            index_col=False
        )
    except Exception as e:
        logging.error("Failed to load csv file, %s", e)
        sys.exit(1)
    logging.info("CSV loaded rows=%d, cols=%d", *df.shape)
    return df

def load_json(
    file_path: Path,
    *,
    orient: str | None = None,    # Expected JSON arrangement ("records", "split", …)
    typ: str = "frame",           # "frame" → DataFrame, "series" → Series
    lines: bool | None = None,    # True if each line is a separate JSON object (NDJSON)
    convert_dates: bool = True,   # Attempt to parse ISO8601 dates
    compression: str | None = "infer",  # "gzip", "bz2", "zip", or "infer"
) -> pd.DataFrame:
    """Read a JSON/NDJSON file into a DataFrame."""
    logging.debug("Reading JSON: %s", file_path)
    df = pd.read_json(
        file_path,
        orient=orient,
        typ=typ,
        lines=lines,
        convert_dates=convert_dates,
        compression=compression,
    )
    logging.info("JSON loaded → rows=%d, cols=%d", *df.shape)
    return df

def load_excel(
    file_path: Path,
    *,
    sheet_name: str | int | list[str] | list[int] | None = 0,  # Which sheet(s) to read
    header: int | None = 0,       # Row to use as column names
    names: list[str] | None = None,
    index_col: int | str | list[int] | None = None,
    usecols: list[int] | list[str] | str | None = None,  # Excel also accepts "A:D"
    dtype: dict[str, str] | None = None,
    nrows: int | None = None,
    skiprows: int | list[int] | None = None,
    engine: str | None = None,    # "openpyxl", "odf", "pyxlsb", …
    na_values: list[str] | str | None = None,
) -> pd.DataFrame:
    """Read an Excel file into a DataFrame (single or multiple sheets)."""
    logging.debug("Reading Excel: %s", file_path)
    df = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        header=header,
        names=names,
        index_col=index_col,
        usecols=usecols,
        dtype=dtype,
        nrows=nrows,
        skiprows=skiprows,
        engine=engine,
        na_values=na_values,
    )
    # pd.read_excel can return a dict if multiple sheets are requested—normalize that:
    if isinstance(df, dict):
        logging.info("Excel loaded: multiple sheets (%d)", len(df))
    else:
        logging.info("Excel loaded → rows=%d, cols=%d", *df.shape)
    return df


# ──────────────────────────────
# Transformer
# ──────────────────────────────
def transform_dataframe(
    df: pd.DataFrame,
    *,
    config: dict[str, Callable[[pd.Series], Any]],
    n_jobs: int | None = None,
    keep_original: bool = True,
) -> pd.DataFrame:
    """
    Build a new DataFrame from *df* using a transformation dictionary

    Parameters
    ----------
    df : pandas.DataFrame
        Source data.  
    config : dict[str, callable]
        Mapping **{new_column_name: func(row) -> value}**.  
        Each *func* receives one pandas.Series (a row of *df*) and
        returns a scalar stored in the output column.  
    n_jobs : int, optional
        CPU cores to use (default = all available-1). Use 1 for sequential.  
    keep_original : bool, optional
        True, include all original columns in the result (default).  
        False, drop original columns; result contains only the newly
                   computed columns (index is preserved).  

    Returns
    -------
    pandas.DataFrame
        Transformed DataFrame.  

    Examples
    --------
    >>> transformer_cfg = {
        "total": lambda r: r["qty"] * r["price"],
        "flag":  lambda r: r["qty"] > 100,
    }
    >>> df_result = transform_dataframe(df, config=transformer_cfg, n_jobs=4)
    """
    if n_jobs is None or n_jobs <= 0:
        n_jobs = max(mp.cpu_count()-1, 1)

    result = df.copy() if keep_original else pd.DataFrame(index=df.index)

    for new_col, func in config.items():
        logging.debug("Computing column '%s' with %s cores", new_col, n_jobs)

        if n_jobs == 1:
            result[new_col] = df.apply(func, axis=1)
        else:
            rows = list(df.itertuples(index=False, name=None))
            computed = Parallel(n_jobs=n_jobs, backend="loky")(
                delayed(func)(pd.Series(row, index=df.columns)) for row in rows
            )
            result[new_col] = computed

        logging.debug("Finished '%s'", new_col)

    return result


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
    logging.debug("Starting process on %s", input_file)

    if not input_file.exists():
        logging.error("File not found: %s", input_file)
        sys.exit(1)

    logging.debug("Finished process")


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
