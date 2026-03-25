import os
import sys
from datetime import datetime
from loguru import logger
from pathlib import Path
from typing import Literal

logger.remove()

TMP_LOGS_PATH = "/tmp/logs"
LOGS_FOLDER = Path(os.getenv("LOG_PATH", TMP_LOGS_PATH))
LOGS_FOLDER.mkdir(parents=True, exist_ok=True)


def get_max_logs_to_keep() -> int:
    if hasattr(get_max_logs_to_keep, "max_logs_to_keep") is False:

        max_logs_to_keep = os.getenv("MAX_LOGS_TO_KEEP", None)
        if max_logs_to_keep is None:
            max_logs_to_keep = 10
            logger.warning(
                "Could not locate value for environment variable MAX_LOGS_TO_KEEP; defaulting to %d.",
                max_logs_to_keep,
            )
        max_logs_to_keep = int(max_logs_to_keep)
        if max_logs_to_keep < 1:
            raise ValueError("MAX_LOGS_TO_KEEP must be >= 1.")
        setattr(get_max_logs_to_keep, "max_logs_to_keep", max_logs_to_keep)
    return getattr(get_max_logs_to_keep, "max_logs_to_keep")


def _init_log(file_name: str, *levels: Literal["INFO", "ERROR"]):
    if len(levels) == 0:
        levels = ("INFO",)

    for level in levels:

        if level == "INFO":
            _file_name = f"{file_name}.log"
        elif level == "ERROR":
            _file_name = f"{file_name}.error"
        else:
            raise ValueError(f"Invalid log level: {level}")
        processing_log_path = LOGS_FOLDER / _file_name
        if processing_log_path.exists():
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            new_log_path = processing_log_path.parent / f"{timestamp}_{_file_name}"
            os.rename(str(processing_log_path), str(new_log_path))

        _trim_logs(level)

        logger.add(processing_log_path, level=level, enqueue=True)

    logger.add(sys.stderr, level="DEBUG", enqueue=True)


def _trim_logs(level):
    max_logs: int = get_max_logs_to_keep()
    ext_to_check = "log" if level == "INFO" else "error"
    logs = list(LOGS_FOLDER.glob(f"*.{ext_to_check}"))
    logs = sorted(logs, key=lambda p: p.stat().st_mtime)
    excess_log_count = len(logs) - max_logs
    if excess_log_count > 0:
        for log_to_delete in logs[:excess_log_count]:
            log_to_delete.unlink()


def initialize_logging(file_name: str):
    _init_log(file_name, "INFO", "ERROR")
    if TMP_LOGS_PATH == str(LOGS_FOLDER):
        logger.warning(
            "Could not locate value for environment variable LOG_PATH; log path to {}.",
            LOGS_FOLDER,
        )
