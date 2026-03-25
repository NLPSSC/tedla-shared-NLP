import os


def get_worker_join_timeout():
    WORKER_JOIN_TIMEOUT_SECONDS = os.getenv("WORKER_JOIN_TIMEOUT_SECONDS")
    if WORKER_JOIN_TIMEOUT_SECONDS is None:
        raise ValueError(
            "WORKER_JOIN_TIMEOUT_SECONDS environment variable must be set."
        )
    worker_join_timeout_seconds = int(WORKER_JOIN_TIMEOUT_SECONDS)
