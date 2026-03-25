from pathlib import Path

import polars as pl


parquet_paths = [
    "part-00001-tid-2641638007781713294-650fddf7-e431-4332-b836-8978e76dda14-22-1-c000.snappy.parquet",
    "part-00000-tid-2641638007781713294-650fddf7-e431-4332-b836-8978e76dda14-21-1-c000.snappy.parquet",
]
root_path = Path(
    "/var/nfs_share/workspaces/ciphi/westerd/tedla/tedla/Y24_notes_to_process_parquet"
)
ps = [root_path / p for p in parquet_paths]

pl.concat(pl.read_parquet(_p) for _p in ps).write_parquet(
    root_path / "combined_notes_to_process.parquet"
)
