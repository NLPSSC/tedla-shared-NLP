from pathlib import Path

from datasources import IterableProjectDataSet


class NotesToProcess(IterableProjectDataSet):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            source_folder="tedla/tedla/notes_to_process_parquet",
            *args,
            **kwargs,
        )

    def is_permitted_dataset(self, dataset_path: Path) -> bool:
        return True


if __name__ == "__main__":
    notes_to_process = NotesToProcess()
    for df in notes_to_process.get(batch_size=10):
        print(df.head())
        break

#                note_id  note_group_id
# 0   591238180697721205              2
# 1  1648864489734375411              2
# 2  1242960489825118281              2
# 3  1993364599658747053              2
# 4  1019760582716127483              2
