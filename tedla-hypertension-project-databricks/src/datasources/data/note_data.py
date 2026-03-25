from glob import glob
import os
import polars as pl
from typing import Callable

from datasources import PolarDataSet


class NoteData(PolarDataSet):

    def __init__(
        self, filter_to_datasets: Callable[[str], bool] | None = None, *args, **kwargs
    ) -> None:
        self._filter_to_datasets: Callable[[str], bool] | None = filter_to_datasets
        note_data_location = os.getenv("NOTE_DATA_LOCATION")
        if note_data_location is None:
            raise ValueError("NOTE_DATA_LOCATION environment variable must be set.")
        if "*" in note_data_location:
            note_parquet_folders: list[str] = glob(
                # "/var/nfs_share/workspaces/ciphi/westerd/tedla/tedla/note_data_*_parquet"
                note_data_location
            )
        else:
            note_parquet_folders = [note_data_location]
        note_parquet_folders = [
            x
            for x in note_parquet_folders
            if filter_to_datasets is None or filter_to_datasets(x)
        ]

        super().__init__(*note_parquet_folders)

    def get(self) -> pl.DataFrame:
        return super().get()
