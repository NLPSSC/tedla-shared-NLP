class WorkerMixin:
    def __init__(self, *args, **kwargs):
        _worker_id = kwargs.get("worker_id", None)
        self._worker_id: str | None = None
        if _worker_id is not None:
            if not (isinstance(_worker_id, int) and _worker_id >= 0):
                raise ValueError("self._worker_id must be None or an integer >= 0")
            self._worker_id = str(_worker_id)
        try:
            super().__init__(*args, **kwargs)
        except:
            super().__init__()

    @property
    def worker_id(self) -> str | None:
        return self._worker_id
