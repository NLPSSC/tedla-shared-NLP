# Cross-process file lock implemented with fcntl on Unix and msvcrt on Windows.


import functools
import os
import platform
import tempfile
import time
from typing import Callable, Optional

# Platform-specific imports
if platform.system() == "Windows":
    import msvcrt
else:
    import fcntl


class FileLock:
    def __init__(
        self, path: str, timeout: Optional[float] = None, delay: float = 0.1
    ) -> None:
        self.path = path
        self.timeout = timeout
        self.delay = delay
        self._file = None
        self._is_windows = platform.system() == "Windows"

    def acquire(self) -> None:
        # Ensure directory exists
        dirpath = os.path.dirname(self.path) or tempfile.gettempdir()
        os.makedirs(dirpath, exist_ok=True)

        # Open the lock file (create if needed)
        self._file = open(self.path, "a+b")

        start = time.time()
        if self._is_windows:

            while True:
                try:
                    # Try non-blocking lock of 1 byte from current position
                    msvcrt.locking(self._file.fileno(), msvcrt.LK_NBLCK, 1)  # type: ignore
                    return
                except OSError:
                    if (
                        self.timeout is not None
                        and (time.time() - start) >= self.timeout
                    ):
                        raise TimeoutError(
                            f"Timeout while acquiring lock on {self.path}"
                        )
                    time.sleep(self.delay)
        else:

            while True:
                try:
                    fcntl.flock(self._file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)  # type: ignore
                    return
                except (BlockingIOError, OSError):
                    if (
                        self.timeout is not None
                        and (time.time() - start) >= self.timeout
                    ):
                        raise TimeoutError(
                            f"Timeout while acquiring lock on {self.path}"
                        )
                    time.sleep(self.delay)

    def release(self) -> None:
        if not self._file:
            return

        try:
            if self._is_windows:

                # Unlock the 1 byte we locked
                try:
                    self._file.seek(0)
                    msvcrt.locking(self._file.fileno(), msvcrt.LK_UNLCK, 1)  # type: ignore
                except OSError:
                    pass
            else:

                try:
                    fcntl.flock(self._file.fileno(), fcntl.LOCK_UN)  # type: ignore
                except OSError:
                    pass
        finally:
            try:
                self._file.close()
            except Exception:
                pass
            self._file = None

    def __enter__(self) -> "FileLock":
        self.acquire()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.release()


def process_lock(lock_path: Optional[str] = None, timeout: Optional[float] = None):
    """
    Decorator that ensures the wrapped function is executed with a per-file
    inter-process lock. If lock_path is None it will default to:
      - SQLITE_DB_PATH + ".lock" if SQLITE_DB_PATH env var is set
      - otherwise a file in the system temp dir named "results_writer.lock"
    timeout (seconds) can be supplied to avoid blocking forever.
    """

    def decorator(fn: Callable):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            path = lock_path
            if path is None:
                sqlite_db = os.environ.get("SQLITE_DB_PATH")
                if sqlite_db:
                    path = f"{sqlite_db}.lock"
                else:
                    path = os.path.join(tempfile.gettempdir(), "results_writer.lock")

            with FileLock(path, timeout=timeout):
                return fn(*args, **kwargs)

        return wrapper

    return decorator
