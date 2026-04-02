from datasources import FullProjectDataSet
from pathlib import Path


class CohortData(FullProjectDataSet):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            source_folder="tedla/tedla/cohort_parquet",
            *args,
            **kwargs,
        )

    def is_permitted_dataset(self, dataset_path: Path) -> bool:
        return True


if __name__ == "__main__":

    df = CohortData().get()
    print(df.head())

#    deid_pat_id       mrn  person_id
# 0       815539  13804349    5558677
# 1       517658  16111171    5817330
# 2       559114  34371286    6328796
# 3       506813  11910064    8857667
# 4       314006  34084558    5328339
