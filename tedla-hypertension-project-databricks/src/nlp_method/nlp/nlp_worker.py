# Worker function that each process will run
from pathlib import Path
from nlp_method.nlp.metrics import MetricsTracking
from nlp_method.nlp.initializer import initialize_nlp_processor
from nlp_method.notes.note_batch_processor import NoteBatchProcessor
from loguru import logger

# Time in seconds that worker processes will wait for new notes to process before
# checking for termination signal. Adjust as needed based on expected time to process
# a batch of notes.
QUEUE_WAIT_TIME = 5  


class NLPWorker:
    def __init__(self, id, queue, ready_signal):
        self._id = id
        self._queue = queue
        self._ready_signal = ready_signal
        self._results_db_path: Path | None = None
        self._nlp_processor: NoteBatchProcessor = initialize_nlp_processor(self._id)
        self._results_db_path = self._nlp_processor.get_results_db_path()
        self._complete: bool = False

    @property
    def worker_id(self) -> int:
        return self._id

    def __call__(self):
        from queue import Empty

        logger.info("Starting worker #{}...", self._id)
        # Initialize inside the child process so resources are owned by it.

        # Signal ready AFTER initialization so the main process only proceeds
        # once the worker is truly able to consume work.
        self._ready_signal.set()

        totals = 0

        with MetricsTracking(f"cycle_time_{str(self._id)}") as metrics_tracking:
            while True:
                try:

                    notes_df = self._queue.get(timeout=QUEUE_WAIT_TIME)
                    if notes_df is None:  # Sentinel value to signal completion
                        self._complete = True
                        logger.info("Worker #{} received completion signal.", self._id)
                        break
                    else:
                        totals += len(notes_df)
                    with metrics_tracking.start_cycle_clock(len(notes_df)):
                        self._nlp_processor(notes_df)
                except Empty:
                    continue
                except Exception as exc:
                    # Fail fast so parent process can detect non-zero exit code
                    # and avoid silent data loss from skipped batches.
                    logger.exception(
                        "Worker #{} encountered an error processing a batch; "
                        "terminating worker to avoid silent data loss. Error: {}",
                        self._id,
                        exc,
                    )
                    raise

            logger.info("Worker #{} complete ({} notes processed).", self._id, totals)

    @property
    def is_complete(self) -> bool:
        return self._complete

    def get_results_db_path(self) -> Path:
        if self._results_db_path is None:
            raise RuntimeError(
                f"Worker #{self._id} has not been started yet "
                "(get_results_db_path called before __call__)."
            )
        return self._results_db_path
