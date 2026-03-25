from pathlib import Path
import time
from typing import List


from common.instance_logr_mixin import InstanceLogrMixin
from common.worker_mixin import WorkerMixin
from nlp_method.results.datastore.results_data_store import ResultsDataStore
from nlp_method.results.result_record import ResultRecord
from nlp_method.results.writer_base import WriterBase
from loguru import logger


class ResultWriter(WriterBase, WorkerMixin, InstanceLogrMixin):

    def __init__(self, *args, **kwargs) -> None:
        self._data_store: ResultsDataStore = ResultsDataStore(*args, **kwargs)
        super().__init__(*args, **kwargs)

    def __call__(self, records: List[ResultRecord]):
        logger.debug("ResultWriter called with {} records", len(records))
        if not records:
            return

        self.log("info", "Starting results writer...")

        start_time: float = time.time()

        # Convert ResultRecord objects to list of dicts
        if not all(isinstance(x, ResultRecord) for x in records):
            raise ValueError("Unexpected entry in records, not type ResultRecord")

        self._data_store.record_results(records)

        end_time: float = time.time()
        self.log(
            "info", "Finished writing results in {} seconds", end_time - start_time
        )
        logger.debug(
            "ResultWriter finished writing {} records in {} seconds",
            len(records),
            end_time - start_time,
        )

    def get_path(self) -> Path:
        return self._data_store.results_path
