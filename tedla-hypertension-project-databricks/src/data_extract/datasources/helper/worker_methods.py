import pandas as pd
from pathlib import Path


def create_note_to_group_lookup(
    idx: int,
    _df: pd.DataFrame,
    map_id_to_group: dict,
    dest_parquet_path: Path,
    write_output: bool = True,
):
    from pathlib import Path

    note_id_membership: pd.DataFrame = _df.pivot(
        index="note_id", columns="note_group_id", values="note_group_id"
    )
    note_id_membership.columns = [
        map_id_to_group[col] for col in note_id_membership.columns
    ]
    note_id_membership = note_id_membership.notna()
    note_id_membership = note_id_membership.astype(bool)

    if write_output is True:
        output_file: Path = (
            dest_parquet_path / f"note_id_to_group_membership_{idx}.parquet"
        )
        note_id_membership.to_parquet(str(output_file))
