from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from nlp_method.results.result_record import ResultRecord


class WriterBase(ABC):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @abstractmethod
    def __call__(self, records: List[ResultRecord]):
        raise NotImplementedError()

    @abstractmethod
    def get_path(self) -> Path:
        raise NotImplementedError()
