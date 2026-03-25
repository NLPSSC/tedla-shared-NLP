import sys
import pandas as pd  # type: ignore
import polars as pl  # type: ignore
from pathlib import Path
from data_extract.datasources.data.note_group_map import NoteGroupMap

sys.path.insert(0, r"/home/westerd/_/research_projects/tedla-hypertension/src")


def create_main_path() -> Path:
    dest_parquet_path = Path(
        "/var/nfs_share/workspaces/ciphi/westerd/tedla/tedla/note_id_to_group_membership"
    )
    dest_parquet_path.mkdir(parents=True, exist_ok=True)
    return dest_parquet_path


def get_map_id_to_group() -> dict[int, str]:
    note_group_map = NoteGroupMap()
    note_group_map_df: pd.DataFrame = note_group_map.get()
    return dict(
        zip(note_group_map_df["note_group_id"], note_group_map_df["note_group"])
    )


if __name__ == "__main__":

    dest_parquet_path = create_main_path()
    map_id_to_group = get_map_id_to_group()

    notes_to_process_source = "/var/nfs_share/workspaces/ciphi/westerd/tedla/tedla/notes_to_process_parquet/part-00000-tid-6779477999508234944-052afa71-ce36-4516-b9dd-e893471994c2-33-1-c000.snappy.parquet"

    # polars uses all CPU cores by default for parquet I/O, deduplication, and pivot.
    # scan_parquet is lazy — projection and unique() are pushed down before any data
    # is materialised, minimising memory usage.
    df = (
        pl.scan_parquet(notes_to_process_source)
        .select(["note_id", "note_group_id"])
        .unique()
        .collect()
    )
    print(f"Unique (note_id, note_group_id) pairs: {len(df):,}")

    # pivot is safe without an aggregate since every pair is already unique.
    membership = (
        df.with_columns(pl.lit(True).alias("present"))
        .pivot(
            values="present",
            index="note_id",
            on="note_group_id",
            aggregate_function="first",
        )
        .fill_null(False)
    )
    del df

    # Rename integer group_id columns to human-readable group names.
    membership = membership.rename({str(k): v for k, v in map_id_to_group.items()})

    output_path: Path = dest_parquet_path / "note_to_groups_map.parquet"
    membership.write_parquet(str(output_path))
    print(f"Written {len(membership):,} rows to {output_path}")
