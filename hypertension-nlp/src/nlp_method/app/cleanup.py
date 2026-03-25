from pathlib import Path
from queue import Empty
from nlp_method.consts import get_worker_join_timeout
from loguru import logger


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


def gc_processes(processes):
    worker_join_timeout_seconds = get_worker_join_timeout()
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
            timeout = 300
            logger.info(
                "Waiting {} seconds for worker process #{} (pid={}) to terminate gracefully before forcefully killing it.",
                timeout,
                idx,
                p.pid,
            )
            p.wait(timeout=timeout)
            p.terminate()
            # failed_workers.append(idx)
            continue

        # if p.exitcode != 0:
        #     logger.error(
        #         "Worker process #{} (pid={}) exited with code {}.",
        #         idx,
        #         p.pid,
        #         p.exitcode,
        #     )
        #     failed_workers.append(idx)
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
    drain_queues(queue)

    gc_processes(processes)

    close_databases(result_dbs)
