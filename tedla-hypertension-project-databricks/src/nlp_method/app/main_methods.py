import os
from pathlib import Path
from queue import Empty
from typing import Any, Generator

from loguru import logger

from nlp_method.__main__ import (
    worker_join_timeout_seconds,
)


def get_number_workers(
    worker_hyper_param: list[int] | None = None,
) -> Generator[int, Any, int] | int:
    """
    Get the number of worker processes from environment variable.
    Reads the NUM_WORKER_PROCESSES environment variable and validates that it
    contains a valid integer value greater than or equal to 1.
    Returns:
        int: The number of worker processes to use.
    Raises:
        ValueError: If NUM_WORKER_PROCESSES is not set, cannot be converted to
            an integer, or is less than 1.
    Example:
        >>> os.environ['NUM_WORKER_PROCESSES'] = '4'
        >>> get_number_workers()
        4
    """
    if worker_hyper_param:
        for x in worker_hyper_param:
            yield x
    num_workers = os.getenv("NUM_WORKER_PROCESSES", None)

    if num_workers is not None:
        num_workers = int(num_workers)
    if num_workers is None or num_workers < 1:
        raise ValueError("Number of worker processes must be >= 1.")
    return num_workers


def get_max_queue_size(
    max_queue_hyper_param: list[int] | None = None,
) -> Generator[int, Any, int] | int:
    """
    Retrieve and validate the maximum worker queue size from environment variables.

    This function reads the MAX_WORKER_QUEUE_SIZE environment variable, converts it to an integer,
    and validates that it is at least 1. If the environment variable is not set or the value is
    invalid, a ValueError is raised.

    Returns:
        int: The maximum queue size for workers, must be >= 1.

    Raises:
        ValueError: If MAX_WORKER_QUEUE_SIZE is not set, cannot be converted to an integer,
                    or is less than 1.

    Environment Variables:
        MAX_WORKER_QUEUE_SIZE: The maximum size of the worker queue (must be >= 1).
    """
    if max_queue_hyper_param:
        for x in max_queue_hyper_param:
            yield x
    max_queue_size = os.getenv("MAX_WORKER_QUEUE_SIZE", None)
    if max_queue_size is not None:
        max_queue_size = int(max_queue_size)
    if max_queue_size is None or max_queue_size < 1:
        raise ValueError("Max queue size must be >= 1.")
    return max_queue_size


def close_databases(database_paths: list[Path]):
    """
    Close all database connections for the given list of database paths.

    This function iterates through the provided list of database paths and attempts to close
    each database connection. If an error occurs while closing a database, it logs the error
    and continues with the next database.

    Args:
        database_paths (list[Path]): A list of Path objects representing the paths to the databases to be closed.
    """
    dbs_to_close = list(
        set(
            [
                y
                for x in list(set(x.parent for x in database_paths))
                for y in x.glob("*.db")
            ]
        )
    )
    for db_path in dbs_to_close:
        try:
            from nlp_method.results.datastore.results_data_store import ResultsDataStore

            ResultsDataStore.close_database(db_path)
            logger.info("Closed database connection for {}", db_path)
        except Exception as e:
            logger.error("Error closing database {}: {}", db_path, e)


def calculate_timing_details(start_time, end_time):
    delta = end_time - start_time
    return {
        "total_seconds": round(delta, 2),
        "total_minutes": round(delta / 60, 2),
        "total_hours": round(delta / 3600, 2),
    }


def log_execution_time(start_time, end_time):
    total_execution_time = calculate_timing_details(start_time, end_time)
    logger.info(
        "Total execution time: {:.2f} seconds / {:.2f} minutes / {:.2f} hours",
        total_execution_time["total_seconds"],
        total_execution_time["total_minutes"],
        total_execution_time["total_hours"],
    )


def gc_processes(processes):
    failed_workers: list[int] = []
    for idx, p in enumerate(processes):
        # Join worker processes with timeout and check for any that are still alive or exited with non-zero exit code
        p.join(timeout=worker_join_timeout_seconds)
        if p.is_alive():
            logger.error(
                "Worker process #{} (pid={}) exceeded join timeout of {} seconds; terminating.",
                idx,
                p.pid,
                worker_join_timeout_seconds,
            )
            p.terminate()
            p.join(timeout=30)
            failed_workers.append(idx)
            continue

        if p.exitcode != 0:
            logger.error(
                "Worker process #{} (pid={}) exited with code {}.",
                idx,
                p.pid,
                p.exitcode,
            )
            failed_workers.append(idx)
        del p

    if failed_workers:
        raise RuntimeError(
            f"The following worker indices exited with a non-zero exit code and "
            f"may have left items in the queue: {failed_workers}"
        )


def drain_queues(queue):
    non_empty_queue_count = 0
    while True:
        try:
            item = queue.get_nowait()  # Non-blocking get
            if item is not None:
                non_empty_queue_count += 1
        except Empty:
            break

    if non_empty_queue_count > 0:
        raise RuntimeError(
            "Found non-None items remaining in the queue after worker completion. "
            f"Remaining non-None items drained: {non_empty_queue_count}."
        )


def cleanup(queue, processes, result_dbs):
    gc_processes(processes)

    drain_queues(queue)

    close_databases(result_dbs)
