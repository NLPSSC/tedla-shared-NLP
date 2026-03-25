from pathlib import Path
import pandas as pd
import sqlite3
import sys
import numpy as np
from loguru import logger


def get_note_id_set(note_ids_mmap_path, results_db_path, cohort_note_data_table):
    def get_note_id_set():
        with sqlite3.connect(results_db_path) as sqlite_cxn:
            cursor = sqlite_cxn.cursor()
            cursor.execute(f"SELECT note_id FROM {cohort_note_data_table};")
            rows = cursor.fetchall()
            note_id_set = set(row[0] for row in rows)
            cursor.close()
            del rows, cursor
        return note_id_set

    note_id_set = get_note_id_set()

    logger.info(f"Total unique note_ids: {len(note_id_set)}")

    def emit_note_id_set_size(note_id_set):
        size_gb = sys.getsizeof(note_id_set) / (1024**3)
        logger.info(f"note_id_set size: {size_gb:.4f} GB")

    emit_note_id_set_size(note_id_set)

    return note_id_set


def read_mmap(note_ids_mmap_path):
    note_ids_set = np.memmap(note_ids_mmap_path, dtype=np.int64, mode="r")
    return note_ids_set


# Save sorted note_ids to disk
def persist_note_id_mmap(note_ids_mmap_path, results_db_path, cohort_note_data_table):
    import os

    if os.path.exists(note_ids_mmap_path) is True:
        logger.info(f"Note IDs mmap file already exists at {note_ids_mmap_path}")
    else:
        note_id_set = get_note_id_set(
            note_ids_mmap_path, results_db_path, cohort_note_data_table
        )
        note_ids = np.array(sorted(note_id_set), dtype=np.int64)
        note_ids.tofile(note_ids_mmap_path)
        logger.info(f"Persisted note IDs to {note_ids_mmap_path}")


def build_note_id_mmap_search(note_ids_mmap_path):

    def is_note_id_present(note_id):
        if hasattr(is_note_id_present, "note_ids") is False:
            note_ids_set = read_mmap(note_ids_mmap_path)
            setattr(is_note_id_present, "note_ids", note_ids_set)

        note_ids_set = getattr(is_note_id_present, "note_ids")
        idx = np.searchsorted(note_ids_set, note_id)
        return idx < len(note_ids_set) and note_ids_set[idx] == note_id

    return is_note_id_present


def process_note_id_to_person_csv(csv_file_path, note_ids_mmap_path):

    logger.info(f"Processing CSV file: {csv_file_path}")

    note_ids_set = read_mmap(note_ids_mmap_path)

    logger.info(f"Filtering note_id_to_person data using mmaped note IDs")

    logger.info(f"Reading CSV file: {csv_file_path}")

    df: pd.DataFrame = pd.read_csv(
        csv_file_path,
        dtype={
            "person_id": np.int64,
            "deid_pat_id": np.int64,
            "mrn": np.int64,
            "note_id": np.int64,
        },
    )

    logger.info(f"CSV file read complete. Total records: {len(df)}")

    # Convert note_ids_set to a set for O(1) lookup
    logger.info(f"Filtering DataFrame for relevant note_ids")
    note_ids_lookup = set(note_ids_set)
    logger.info(f"Total note_ids for lookup: {len(note_ids_lookup)}")
    df = df[df["note_id"].isin(note_ids_lookup)]
    logger.info(f"Filtering complete. Records after filtering: {len(df)}")

    output_path = f"/home/westerd/_/project_data/tedla-hypertension/note_id_to_person_output/{Path(csv_file_path).name}.filtered.parquet"
    logger.info(f"Writing DataFrame to parquet file: {output_path}")
    df.to_parquet(output_path, index=False)
    logger.info(f"Successfully wrote {len(df)} records to {output_path}")
