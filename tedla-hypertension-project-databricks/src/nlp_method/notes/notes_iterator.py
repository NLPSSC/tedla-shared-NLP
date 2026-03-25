import os
import pandas as pd
import polars as pl
from concurrent import futures
from typing import Any, Generator
from data_extract.datasources.note_data_aggration import NoteDataAggregator
from data_extract.datasources.data.note_data import NoteData
from loguru import logger

from nlp_method.results.result_record import SourceData

EXPECTED_JOINED_TABLE_NOTES: list[str] = [
    "note_id",
    "note_text",
    "batch_group",
    "problem_list_notes_group",
    "outpatient_notes_group",
    "communication_encounter_notes_group",
    "inpatient_notes_group",
    "admission_notes_group",
    "emergency_department_notes_group",
    "ecg_impression_notes_group",
    "discharge_summary_notes_group",
    "person_id",
    "x_part_num",
    "x_uniq",
    "note_date",
    "visit_occurrence_id",
    "is_patient_communication",
    "note_within_visit",
    "visit_start_date",
    "visit_end_date",
]


def get_default_note_iterator_batch_size(
    note_iterator_hyper_param: list[int] | None = None,
) -> Generator[int, Any, int] | int:
    if note_iterator_hyper_param:
        for x in note_iterator_hyper_param:
            yield x
    batch_size_env = os.getenv("NOTE_ITERATOR_BATCH_SIZE", None)
    if batch_size_env is None:
        raise ValueError("NOTE_ITERATOR_BATCH_SIZE environment variable must be set.")
    try:
        batch_size = int(batch_size_env)
    except ValueError as exc:
        raise ValueError(
            "NOTE_ITERATOR_BATCH_SIZE environment variable must be an integer."
        ) from exc
    if batch_size < 1:
        raise ValueError("NOTE_ITERATOR_BATCH_SIZE must be at least 1.")
    return batch_size


def get_max_loader_workers() -> int:
    max_loader_workers_env = os.getenv("MAX_LOADER_WORKERS", None)
    if max_loader_workers_env is None:
        raise ValueError("MAX_LOADER_WORKERS environment variable must be set.")
    try:
        max_loader_workers = int(max_loader_workers_env)
    except ValueError as exc:
        raise ValueError(
            "MAX_LOADER_WORKERS environment variable must be an integer."
        ) from exc
    if max_loader_workers < 1:
        raise ValueError("MAX_LOADER_WORKERS must be at least 1.")
    return max_loader_workers


class NotesIterator:

    def __init__(
        self,
        note_data: NoteData,
        note_iterator_batch_size: int,
        debug_max_iterations: int | None = None,
    ) -> None:

        batch_size = note_iterator_batch_size
        if batch_size is None:
            raise ValueError("NotesIterator batch_size cannot be None")
        batch_size = int(batch_size)
        logger.info("Initializing NotesIterator with batch size {}...", batch_size)
        self._note_iter: Generator[pl.DataFrame, None, None] = note_data.to_batches(
            batch_size=batch_size
        )
        self._note_data_aggr: NoteDataAggregator = NoteDataAggregator()
        self._current_batch_group_num = None
        self._max_group_num = None
        self._debug_max_iterations: int | None = debug_max_iterations

    def _build_note_data(
        self, note_data_df: pd.DataFrame | pl.DataFrame, batch_num: int
    ) -> pd.DataFrame:

        if isinstance(note_data_df, pl.DataFrame):
            note_data_df = note_data_df.with_columns(
                pl.lit(batch_num).alias("batch_group")
            )
        else:
            note_data_df["batch_group"] = batch_num

        note_data_with_metadata: pd.DataFrame = self._note_data_aggr.append_metadata(
            note_data_df
        )

        assert all(
            col in note_data_with_metadata.columns
            for col in EXPECTED_JOINED_TABLE_NOTES
        ), f"Joined table is missing expected columns. Expected: {EXPECTED_JOINED_TABLE_NOTES}, Actual: {note_data_with_metadata.columns.tolist()}"

        # Rename to is_note_within_visit
        if "note_within_visit" in note_data_with_metadata.columns:
            note_data_with_metadata = note_data_with_metadata.rename(
                columns={"note_within_visit": "is_note_within_visit"}
            )

        # Default is_note_within_visit to False if not present
        if "is_note_within_visit" not in note_data_with_metadata.columns:
            note_data_with_metadata["is_note_within_visit"] = (
                False  # or another default value
            )

        source_data_columns = SourceData.columns()
        note_data_with_metadata = note_data_with_metadata[source_data_columns]
        assert all(
            col in note_data_with_metadata.columns for col in source_data_columns
        ), f"Final table is missing expected columns. Expected: {source_data_columns}, Actual: {note_data_with_metadata.columns.tolist()}"
        assert (
            "note_text" in note_data_with_metadata.columns
        ), "Final table is missing 'note_text' column."
        return note_data_with_metadata

    def __iter__(self) -> Generator[pd.DataFrame, None, None]:

        max_loader_workers = get_max_loader_workers()
        max_pending_futures = max_loader_workers * 2

        with futures.ThreadPoolExecutor(max_workers=max_loader_workers) as executor:

            total_processed = 0
            remaining_debug_iterations = self._debug_max_iterations
            future_results: set[futures.Future] = set()
            for batch_num, note_data_df in enumerate(self._note_iter):
                future_results.add(
                    executor.submit(self._build_note_data, note_data_df, batch_num)
                )

                if len(future_results) >= max_pending_futures:
                    done, _ = futures.wait(
                        future_results, return_when=futures.FIRST_COMPLETED
                    )
                    for future in done:
                        future_results.discard(future)
                        _df: pd.DataFrame = future.result()
                        dataframe_size: int = len(_df)
                        total_processed += dataframe_size
                        logger.info(
                            "Yielding {} rows with {} sent",
                            dataframe_size,
                            total_processed,
                        )
                        yield _df

                if remaining_debug_iterations is not None:
                    remaining_debug_iterations -= 1
                    if remaining_debug_iterations <= 0:
                        break

                done, _ = futures.wait(future_results, timeout=1)
                for future in done:
                    future_results.discard(future)
                    _df: pd.DataFrame = future.result()
                    dataframe_size: int = len(_df)
                    total_processed += dataframe_size
                    logger.info(
                        "Yielding {} rows with {} sent",
                        dataframe_size,
                        total_processed,
                    )
                    yield _df

            for future in futures.as_completed(future_results):
                df: pd.DataFrame = future.result()
                dataframe_size = len(df)
                total_processed += dataframe_size
                logger.info(
                    "Yielding {} rows with {} sent",
                    dataframe_size,
                    total_processed,
                )
                yield df
