import os
from loguru import logger
from contextlib import contextmanager
from pathlib import Path
from time import time


class MetricsTracking:

    def __init__(self, file_name: str) -> None:
        metrics_path = os.getenv("METRICS_PATH", None)
        if metrics_path is None:
            logger.warning(
                "METRICS_PATH is not defined; cycle-time metrics will be disabled for worker {}.",
                file_name,
            )
            self._metrics_file = None
            self._fh = None
            self._start_time = None
            return

        metrics_path = Path(metrics_path)
        metrics_path.mkdir(parents=True, exist_ok=True)
        self._metrics_file: Path | None = metrics_path / f"{file_name}.csv"
        logger.info("Monitoring metrics for {}", self._metrics_file)
        self._fh = open(self._metrics_file, "w", buffering=1)
        self._start_time = None

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        self.cleanup()

    @contextmanager
    def start_cycle_clock(self, number_notes: int):
        if self._fh is None:
            yield
            return

        self._start_time = time()
        yield
        total_time = time() - self._start_time
        self._fh.write(f"{number_notes},{total_time}\n")
        self._fh.flush()

    def cleanup(self):
        if self._fh is not None:
            self._fh.close()
