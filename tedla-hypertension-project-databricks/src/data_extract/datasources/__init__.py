from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Generator, cast, overload
import polars as pl
import pandas as pd

from loguru import logger


class ProjectDataSet(ABC):

    def __init__(self, source_folder: Path | str, load_all: bool = True) -> None:

        if isinstance(source_folder, str):
            if "*" in source_folder:
                # need to gather all folders that match the pattern and load data from them
                pattern: str = Path(source_folder).name
                self._source_folders: list[Path] = [
                    x
                    for x in list(Path(source_folder).parent.glob(pattern))
                    if self.is_permitted_dataset(x)
                ]
            else:
                self._source_folders: list[Path] = [Path(source_folder)]
        else:
            self._source_folders: list[Path] = [source_folder]
        self._load_all: bool = load_all
        self._df: pd.DataFrame | None = None
        self._df_iterator: Generator[pd.Series[Any], Any, None] | None = None
        super().__init__()

    @abstractmethod
    def is_permitted_dataset(self, dataset_path: Path) -> bool:
        raise NotImplementedError("Subclasses must implement this method")

    def get_total_rows(self) -> int:
        total_rows: int = 0
        for source_folder in self._source_folders:
            for file in source_folder.glob("*.parquet"):
                df = pd.read_parquet(file, columns=[])
                total_rows += len(df)
        return total_rows

    @overload
    def get(self) -> pd.DataFrame | Generator[pd.Series, Any, None]: ...

    @overload
    def get(self, batch_size: int) -> Generator[pd.DataFrame, Any, None]: ...

    def get(
        self, batch_size: int | None = None
    ) -> (
        pd.DataFrame
        | Generator[pd.Series, Any, None]
        | Generator[pd.DataFrame, Any, None]
    ):
        self.load()
        if self._load_all:
            if self._df is None:
                raise ValueError("Dataframe not loaded")
            return self._df
        else:
            if self._df_iterator is None:
                raise ValueError("Dataframe iterator not loaded")
            if batch_size is None:
                return self._df_iterator
            else:

                def batch_generator():
                    batch = []
                    assert (
                        self._df_iterator is not None
                    ), "Dataframe iterator not loaded"
                    for row in self._df_iterator:
                        batch.append(row)
                        if len(batch) == batch_size:
                            yield pd.DataFrame(batch)
                            batch = []
                    if batch:
                        yield pd.DataFrame(batch)

                return batch_generator()

    def load(self):
        if self._load_all:
            self._df = self._load_all_data()
        else:
            self._df_iterator = self._get_data_iterator()

    def _load_all_data(self):
        # find all parquet files int the source folder and load them into a single dataframe
        all_files: list[Path] = [
            file
            for source_folder in self._source_folders
            for file in source_folder.glob("*.parquet")
        ]
        return ProjectDataSet._load_files(all_files)

    def _get_data_iterator(self) -> Generator[pd.Series, Any, None]:
        # find all parquet files int the source folder and return an iterator that yields dataframes
        all_files: list[Path] = [
            file
            for source_folder in self._source_folders
            for file in source_folder.glob("*.parquet")
        ]

        def row_generator():
            import pyarrow.parquet as pq

            for file in all_files:
                parquet_file = pq.ParquetFile(file)
                for batch in parquet_file.iter_batches():
                    df = batch.to_pandas()
                    for _, row in df.iterrows():
                        yield row

        return row_generator()

    @staticmethod
    def _load_files(files: list[Path]) -> pd.DataFrame:
        import pandas as pd

        dfs = []
        for file in files:
            dfs.append(pd.read_parquet(file))
        return pd.concat(dfs, ignore_index=True)


class IterableProjectDataSet(ProjectDataSet):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(load_all=False, *args, **kwargs)


class FullProjectDataSet(ProjectDataSet):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(load_all=True, *args, **kwargs)

    def get(self) -> pd.DataFrame:  # type: ignore
        return cast(pd.DataFrame, super().get())


class PandasDataSet:
    def __init__(self, source_path: Path | str, col_map: dict[str, str] = {}) -> None:
        self._source_path = Path(source_path)
        self._df = pd.read_parquet(self._source_path)
        if len(col_map) > 0:
            self._df = self._df.rename(columns=col_map)

    def get(self) -> pd.DataFrame:
        return pd.read_parquet(self._source_path)


class PolarDataSet:

    def __init__(
        self, *source_folder: Path | str, col_map: dict[str, str] = {}
    ) -> None:

        logger.info(
            f"[{self.__class__.__name__}] Initializing dataset from source folders: {source_folder}..."
        )

        source_folders: list[Path] = [Path(x) for x in list(source_folder)]

        _files: list[Path] = [
            f for f in source_folders if f.is_file() and f.suffix == ".parquet"
        ]
        _folders: list[Path] = [f for f in source_folders if f.is_dir()]
        parquet_files: list[Path] = [
            parquet_file
            for src_fldr in _folders
            for parquet_file in Path(src_fldr).glob("**/*.parquet")
        ] + _files

        logger.info(
            f"[{self.__class__.__name__}] Loading data from {len(parquet_files)} parquet files..."
        )

        self._df: pl.DataFrame = pl.read_parquet(
            parquet_files,
            use_pyarrow=True,
            memory_map=True,
        )
        if col_map:
            self._df = self._df.rename(col_map)

        logger.info(f"[{self.__class__.__name__}] Data loaded successfully.")

    def get(self) -> pl.DataFrame:
        return self._df

    def to_batches(self, batch_size: int) -> Generator[pl.DataFrame, None, None]:
        total_rows = self._df.height
        for start in range(0, total_rows, batch_size):
            yield self._df.slice(start, batch_size)
