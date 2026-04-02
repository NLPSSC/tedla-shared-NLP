from pathlib import Path


from datasources import FullProjectDataSet


class NoteGroupMap(FullProjectDataSet):

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(
            source_folder="tedla/tedla/note_group_map_parquet",
            *args,
            **kwargs,
        )

    def is_permitted_dataset(self, dataset_path: Path) -> bool:
        return True


if __name__ == "__main__":

    note_group_map = NoteGroupMap()
    df = note_group_map.get()
    print(df.head())

    #       note_group_id                              note_group
    # 0         1                           admission_notes_group
    # 1         2             communication_encounter_notes_group
    # 2         3                   discharge_summary_notes_group
    # 3         4                      ecg_impression_notes_group
