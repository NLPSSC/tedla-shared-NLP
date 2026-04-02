import os
import polars as pl
import pandas as pd

from datasources import PolarDataSet
from datasources.data.data_to_process import NoteMetaData
from datasources.data.note_data import NoteData
from datasources.data.note_to_visit_date import NoteToVisitDetails


class NoteToGroupsMap(PolarDataSet):

    def __init__(self) -> None:
        path = os.getenv("NOTE_TO_GROUPS_MAP_PATH")
        raise ValueError("Environment variable NOTE_TO_GROUPS_MAP_PATH is not set.")
        super().__init__(path)

    def get(self) -> pl.DataFrame:
        return super().get()


class NoteDataAggregator:

    def __init__(self) -> None:
        self._note_to_groups_map = NoteToGroupsMap()
        self._note_metadata = NoteMetaData()
        self._note_visit_data = NoteToVisitDetails()

    def append_metadata(
        self, note_data_df: pd.DataFrame | pl.DataFrame
    ) -> pd.DataFrame:

        note_to_groups_map_df: pl.DataFrame = self._note_to_groups_map.get()
        note_groups = (
            pl.from_pandas(note_data_df)
            if isinstance(note_data_df, pd.DataFrame)
            else note_data_df
        ).join(
            note_to_groups_map_df,
            left_on="note_id",
            right_on="note_id",
            how="inner",
        )

        note_groups_and_metadata = note_groups.join(
            self._note_metadata.get(), on="note_id", how="inner"
        )

        note_groups_meta_and_visits = note_groups_and_metadata.join(
            self._note_visit_data.get(),
            # on=["note_id"],
            on=["note_id", "visit_occurrence_id"],
            how="left",
        )

        joined_table: pd.DataFrame = note_groups_meta_and_visits.to_pandas()

        return joined_table


if __name__ == "__main__":
    note_full_data_df: pd.DataFrame = NoteDataAggregator().append_metadata(
        NoteData().get()
    )
    print(note_full_data_df.head())
    print(note_full_data_df.columns)

#                note_id      note_text  problem_list_notes_group     ...     note_within_visit   visit_start_date    visit_end_date
# 0  5890362938063667721      ...        False                        ...     None                NaT                 NaT
# 1  5958627857156858033      ...        False                        ...     None                NaT                 NaT
# 2  5848398355262889725      ...        False                        ...     None                NaT                 NaT
# 3  5940223292207940730      ...        False                        ...     None                NaT                 NaT
# 4  5855437907210811514      ...        False                        ...     None                NaT                 NaT


# note_id
# note_text
# problem_list_notes_group
# outpatient_notes_group
# communication_encounter_notes_group
# inpatient_notes_group
# admission_notes_group
# emergency_department_notes_group
# ecg_impression_notes_group
# discharge_summary_notes_group
# person_id
# x_part_num
# x_uniq
# note_date
# visit_occurrence_id
# is_patient_communication
# note_within_visit
# visit_start_date
# visit_end_date
