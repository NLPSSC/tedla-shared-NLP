import os

import polars as pl

from datasources import PolarDataSet


class NoteMetaData(PolarDataSet):

    def __init__(self, *args, **kwargs) -> None:
        data_to_process_dataset = os.getenv("DATA_TO_PROCESS_DATASET")
        if data_to_process_dataset is None:
            raise ValueError(
                "DATA_TO_PROCESS_DATASET environment variable must be set."
            )

        super().__init__(
            data_to_process_dataset
        )


if __name__ == "__main__":

    data_to_process = NoteMetaData()
    df: pl.DataFrame = data_to_process.get()

    dupes = (
        df.group_by(["x_uniq", "x_part_num"])
        .agg(pl.count().alias("count"))
        .filter(pl.col("count") > 1)
    )
    print(dupes)


#     # ...existing code...
#     print(df.filter(pl.col("x_uniq") == '3045540428').head())
# # ...existing code...

# ┌─────────────────────┬───────────┬────────────┬────────────┬────────────┬─────────────────────┬──────────────────────────┬───────────────────┐
# │ note_id             ┆ person_id ┆ x_part_num ┆ x_uniq     ┆ note_date  ┆ visit_occurrence_id ┆ is_patient_communication ┆ note_within_visit │
# │ ---                 ┆ ---       ┆ ---        ┆ ---        ┆ ---        ┆ ---                 ┆ ---                      ┆ ---               │
# │ i64                 ┆ i64       ┆ i32        ┆ str        ┆ date       ┆ i64                 ┆ bool                     ┆ bool              │
# ╞═════════════════════╪═══════════╪════════════╪════════════╪════════════╪═════════════════════╪══════════════════════════╪═══════════════════╡
# │ 5838851739043601132 ┆ 12021053  ┆ 1          ┆ 1258553849 ┆ 2021-09-09 ┆ 318093416           ┆ false                    ┆ null              │
# │ 5962036047194007624 ┆ 9912263   ┆ 1          ┆ 163771959  ┆ 2020-03-12 ┆ 245542556           ┆ false                    ┆ null              │
# │ 5906161477316100639 ┆ 6900390   ┆ 1          ┆ 1169560601 ┆ 2021-07-09 ┆ 306711047           ┆ false                    ┆ null              │
# │ 5859002541767698329 ┆ 13733486  ┆ null       ┆ 32730366   ┆ 2021-11-09 ┆ null                ┆ false                    ┆ null              │
# │ 5890362938063667721 ┆ 7579845   ┆ 3          ┆ 66818372   ┆ 2018-02-12 ┆ null                ┆ false                    ┆ null              │
# └─────────────────────┴───────────┴────────────┴────────────┴────────────┴─────────────────────┴──────────────────────────┴───────────────────┘
