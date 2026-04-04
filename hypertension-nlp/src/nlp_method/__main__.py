from pathlib import Path
from time import time
import multiprocessing as mp
import os
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")  # Reads .env from current working directory

from nlp_method.app.cleanup import cleanup
from datasources.data.note_data import NoteData
from nlp_method.app.nlp_worker import create_nlp_workers
from nlp_method.app.log_time import log_execution_time
from nlp_method.notes.notes_iterator import NotesIterator
from loguru import logger


def main(
    note_data: NoteData,
    num_workers: int,
    max_queue_size: int,
    note_iterator_batch_size: int,
    num_test_iterations: int | None = None,
):

    total_start_time = time()

    # Create a queue with max size 15
    queue = mp.Queue(maxsize=max_queue_size)

    logger.info("Creating {} NLP worker processes...", num_workers)

    # Create NLP worker processes, which monitors the queue for new notes to process and processes them in parallel.
    # Each worker will signal when it is ready before the main process continues to put notes in the queue.
    nlp_workers, processes = create_nlp_workers(num_workers, queue)

    logger.info("{} NLP worker processes created.", num_workers)

    # Iterate through notes in batches and put them in the queue for workers to process
    notes_loaded = 0
    for notes_df in NotesIterator(
        note_data,
        note_iterator_batch_size=note_iterator_batch_size,
        debug_max_iterations=num_test_iterations,
    ):
        notes_loaded += len(notes_df)
        logger.info("Loaded {} notes so far...", notes_loaded)
        queue.put(notes_df)

    # Send sentinel values to signal workers to stop
    for _ in range(len(processes)):
        queue.put(None)

    # result_dbs -> list of sqlite dbs created by each worker process to store results before they are merged into a final output
    result_dbs: list[Path] = [x.get_results_db_path() for x in nlp_workers]

    # Wait for all processes to complete

    cleanup(queue, processes, result_dbs)

    total_time = time() - total_start_time
    logger.success(
        "Completed in {} secs / {} mins / {} hours",
        total_time,
        total_time / 60,
        total_time / 3600,
    )


if __name__ == "__main__":

    from common.logr import initialize_logging

    initialize_logging("tedla-hypertension-nlp")

    note_data: NoteData = NoteData(filter_to_datasets=None)
    nlp_config = {
        "num_test_iterations": None,
        "note_iterator_batch_size": int(os.getenv("NOTE_ITERATOR_BATCH_SIZE", 1000)),  # type: ignore
        "max_queue_size": 128,
        "num_workers": int(os.getenv("NUM_WORKER_PROCESSES", 8)),
        "start_time": time(),
    }

    logger.info(
        "Settings: {}",
        ", ".join([f"{k}: {v}" for k, v in nlp_config.items()]),
    )

    main(
        note_data=note_data,
        num_workers=nlp_config["num_workers"],  # type: ignore
        max_queue_size=nlp_config["max_queue_size"],  # type: ignore
        num_test_iterations=nlp_config["num_test_iterations"],  # type: ignore
        note_iterator_batch_size=nlp_config["note_iterator_batch_size"],  # type: ignore
    )
    end_time = time()
    nlp_config["end_time"] = end_time

    log_execution_time(nlp_config["start_time"], end_time)
