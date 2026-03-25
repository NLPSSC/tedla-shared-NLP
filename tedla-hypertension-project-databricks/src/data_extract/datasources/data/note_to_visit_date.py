import os
from data_extract.datasources import PolarDataSet


class NoteToVisitDetails(PolarDataSet):

    def __init__(self) -> None:
        path = os.getenv(
            "NOTE_TO_VISIT_DATE_PATH",
            "/var/nfs_share/workspaces/ciphi/westerd/tedla/tedla/vw_note_to_visit_date_parquet/part-00000-tid-9007553038768159611-d9ac5572-19a4-4313-9f19-2bb513de211d-3663-1-c000.snappy.parquet",
        )
        super().__init__(path)


if __name__ == "__main__":
    note_to_visit_details = NoteToVisitDetails()
    print(note_to_visit_details.get().head())

# ┌──────────────────────┬─────────────────────┬──────────────────┬────────────────┐
# │ note_id              ┆ visit_occurrence_id ┆ visit_start_date ┆ visit_end_date │
# │ ---                  ┆ ---                 ┆ ---              ┆ ---            │
# │ i64                  ┆ i64                 ┆ date             ┆ date           │
# ╞══════════════════════╪═════════════════════╪══════════════════╪════════════════╡
# │ 1889818786517079220  ┆ 29950753            ┆ 2017-11-21       ┆ 2017-11-21     │
# │ 5917616847991062525  ┆ 29950753            ┆ 2017-11-21       ┆ 2017-11-21     │
# │ -6141386412346192830 ┆ 29950948            ┆ 2017-11-16       ┆ 2017-11-16     │
# │ 1560307618683562463  ┆ 29950948            ┆ 2017-11-16       ┆ 2017-11-16     │
# │ -5243982918437738291 ┆ 29950997            ┆ 2017-11-10       ┆ 2017-11-10     │
# └──────────────────────┴─────────────────────┴──────────────────┴────────────────┘
