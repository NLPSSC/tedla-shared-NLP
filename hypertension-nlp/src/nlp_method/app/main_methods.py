import os
from typing import Any, Generator


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
