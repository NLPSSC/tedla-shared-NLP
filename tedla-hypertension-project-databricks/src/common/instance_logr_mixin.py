from typing import Literal
from loguru import logger


class InstanceLogrMixin:

    def __init__(self, *args, **kwargs) -> None:
        id = kwargs.get("id", None)
        self._id: str | None = None
        if id is not None:
            self._id = str(id)

    def log(self, log_type: Literal["info", "error"], msg: str, *args):
        derived_class_name: str = self.__class__.__name__
        formatted_message: str = msg.format(*args)
        log_method = None
        if log_type == "info":
            log_method = logger.info
        elif log_type == "error":
            log_method = logger.error
        else:
            raise ValueError(f"log method not defined: {log_type}")

        if self._id is not None:
            log_method("[{} #{}] {}", derived_class_name, self._id, formatted_message)
        else:
            log_method("[{}] {}", derived_class_name, formatted_message)
