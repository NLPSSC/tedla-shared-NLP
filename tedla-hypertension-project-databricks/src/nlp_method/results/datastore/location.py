from common.worker_mixin import WorkerMixin


from loguru import logger


import atexit
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Callable


class DataStoreLocation(WorkerMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._specific_folder_name = None
        self._root_db_path: Path = self._get_root_db_path()

        self._file_lock: Path = self._root_db_path / f"results.lock"

        self._results_log: Path = self._init_results_audit_log()

        self._worker_results_path: Path = (
            Path(self._root_db_path) / self.get_folder_name()
        )
        self._worker_results_path.mkdir(parents=True, exist_ok=True)

    def __del__(self):
        """
        Destructor method called when the instance is about to be destroyed.

        Attempts to release resources associated with the folder name by calling
        the `_release_folder_name` method. If an exception occurs during this process,
        it logs a warning message with the exception details.

        Note:
            The `__del__` method is called when the object's reference count reaches zero
            and it is about to be garbage collected. However, the exact timing of its
            invocation is not guaranteed and may vary depending on the Python implementation
            and the presence of circular references.
        """
        try:
            logger.info("Decrementing file lock for worker {}", self.worker_id)
            current_lock_count = self._manage_file_lock(lambda x: x - 1)
            if current_lock_count == 0:
                self._unlink_lock_file()
        except Exception as e:
            logger.warning(f"Exception in __del__ of ResultDataStorePath: {e}")

    @property
    def results_audit_log_path(self) -> Path:
        return self._results_log

    @property
    def worker_results_path(self) -> Path:
        db_path: Path = self._worker_results_path / f"results_{self.worker_id}.db"
        return db_path

    def _get_root_db_path(self) -> Path:
        _root_db_path = os.getenv("SQLITE_DB_PATH", None)
        if _root_db_path is None:
            raise ValueError("SQLITE_DB_PATH environment variable is not defined.")

        _root_db_path = Path(_root_db_path)
        _root_db_path.mkdir(parents=True, exist_ok=True)
        if _root_db_path.is_dir() is False:
            raise ValueError(
                f"SQLITE_DB_PATH {_root_db_path} is not a valid directory path."
            )

        return Path(_root_db_path)

    def _init_results_audit_log(self) -> Path:
        _results_log: Path = self._root_db_path / f"results_audit_log.json"

        if _results_log.exists() is False:
            logger.info(
                "Results log for worker {} will be stored at {}",
                self.worker_id,
                _results_log,
            )
            with open(_results_log, "w") as json_log_fh:
                json.dump([], json_log_fh)

        return _results_log

    def get_folder_name(self) -> str:

        if self._specific_folder_name is not None:
            return self._specific_folder_name

        logger.info("Incrementing file lock for worker {}", self.worker_id)
        lock_count = self._manage_file_lock(lambda x: x + 1)

        folder_name = None
        if lock_count == 1:

            results_log_json = self.get_audit_log_data()

            current_datetime = datetime.now()
            folder_name = current_datetime.strftime("results_%Y%m%d_%H%M%S")

            item = {
                "result_folder_name": folder_name,
                "create_datetime": current_datetime.isoformat(),
            }

            results_log_json.append(item)

            with open(self._results_log, "w") as json_log_fh:
                json.dump(results_log_json, json_log_fh, indent=2)
                json_log_fh.flush()

        self._specific_folder_name = self.get_latest_results_folder_name()
        assert (
            self._specific_folder_name is not None
        ), "Folder name should have been set"
        return self._specific_folder_name

    def get_latest_results_folder_name(self):
        results_log_json = self.get_audit_log_data()
        assert isinstance(results_log_json, list), "Results log JSON should be a list"
        assert (
            len(results_log_json) > 0
        ), "Results log JSON should contain at least one entry"
        if len(results_log_json) > 0:
            assert (
                "result_folder_name" in results_log_json[0]
            ), "Expected result log entries to contain 'result_folder_name'"
            assert (
                "create_datetime" in results_log_json[0]
            ), "Expected result log entries to contain 'create_datetime'"
        results_log_json.sort(key=lambda x: x["create_datetime"], reverse=True)
        results_folder_name_str = results_log_json[0]["result_folder_name"]
        return results_folder_name_str
    
    def get_latest_results_folder_path(self) -> Path:
        latest_folder_name = self.get_latest_results_folder_name()
        latest_folder_path = self._root_db_path / latest_folder_name
        return latest_folder_path

    def get_audit_log_data(self):
        with open(self._results_log, "r") as json_log_fh:
            results_log_json = json.load(json_log_fh)
        return results_log_json

    def _manage_file_lock(self, file_lock_count_method: Callable[[int], int]) -> int:
        folder_name: str | None = None
        current_lock_count = self._update_lock_count(file_lock_count_method)

        return current_lock_count

    def _unlink_lock_file(self):
        if self._file_lock.exists():
            try:
                self._file_lock.unlink()
                logger.info("Unlinked file lock at {}", self._file_lock)
            except Exception as e:
                logger.warning(f"Failed to unlink file lock at {self._file_lock}: {e}")

    def _update_lock_count(self, file_lock_count_method):
        from nlp_method.results.FileLock import FileLock

        if self._file_lock.exists() is False:
            self._file_lock.touch(exist_ok=True)

        lock = FileLock(str(self._file_lock) + ".lck", timeout=30)
        lock.acquire()
        try:
            with open(self._file_lock, "r+") as f:
                value = f.read().strip()
                try:
                    current_lock_count = int(value)
                except ValueError:
                    current_lock_count = 0
                current_lock_count = file_lock_count_method(current_lock_count)
                assert current_lock_count >= 0, "File lock count cannot be negative"
                f.seek(0)
                f.truncate()
                f.write(str(current_lock_count))
                f.flush()
        finally:
            lock.release()
        return current_lock_count
