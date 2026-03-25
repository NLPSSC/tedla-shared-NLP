import os

from datasources import PandasDataSet


class NoteGroupToTermMap(PandasDataSet):

    col_maps: dict[str, str] = {
        "notes_admissions": "admission_notes_group",
        "notes_communication_encounter": "communication_encounter_notes_group",
        "notes_discharge_summary": "discharge_summary_notes_group",
        "notes_ecg_impression": "ecg_impression_notes_group",
        "notes_emergency_department": "emergency_department_notes_group",
        "notes_inpatient": "inpatient_notes_group",
        "notes_outpatient": "outpatient_notes_group",
        "notes_problem_lists": "problem_list_notes_group",
    }

    def __init__(self) -> None:
        path = os.getenv(
            "NOTE_GROUP_TO_TERM_PATH",
            "/var/nfs_share/workspaces/ciphi/westerd/tedla/tedla/note_group_to_term_parquet/part-00000-tid-9122224030368219261-69b4115d-c0d4-409f-aaeb-fabe8b40831a-7387-1-c000.snappy.parquet",
        )
        super().__init__(
            path,
            col_map=NoteGroupToTermMap.col_maps,
        )

    @staticmethod
    def note_groups():
        return list(NoteGroupToTermMap.col_maps.values())


if __name__ == "__main__":
    note_group_to_term_map = NoteGroupToTermMap()
    df = note_group_to_term_map.get()
    print(df.head())
    for c in df.columns:
        print(c)

# ┌────────────────────┬────────────────────┬──────────────────┬────────────────────┬───┬───────────────────┬─────────────────┬──────────────────┬───────────────────┐
# │ search_term_to_not ┆ search_term        ┆ notes_admissions ┆ notes_communicatio ┆ … ┆ notes_emergency_d ┆ notes_inpatient ┆ notes_outpatient ┆ notes_problem_lis │
# │ e_groups_id        ┆ ---                ┆ ---              ┆ n_encounter        ┆   ┆ epartment         ┆ ---             ┆ ---              ┆ ts                │
# │ ---                ┆ str                ┆ i64              ┆ ---                ┆   ┆ ---               ┆ i64             ┆ i64              ┆ ---               │
# │ i64                ┆                    ┆                  ┆ i64                ┆   ┆ i64               ┆                 ┆                  ┆ i64               │
# ╞════════════════════╪════════════════════╪══════════════════╪════════════════════╪═══╪═══════════════════╪═════════════════╪══════════════════╪═══════════════════╡
# │ 1                  ┆ heart failure with ┆ 1                ┆ 0                  ┆ … ┆ 1                 ┆ 1               ┆ 1                ┆ 1                 │
# │                    ┆ reduced eje…       ┆                  ┆                    ┆   ┆                   ┆                 ┆                  ┆                   │
# │ 2                  ┆ hfref              ┆ 1                ┆ 0                  ┆ … ┆ 1                 ┆ 1               ┆ 1                ┆ 1                 │
# │ 3                  ┆ heart failure with ┆ 1                ┆ 0                  ┆ … ┆ 1                 ┆ 1               ┆ 1                ┆ 1                 │
# │                    ┆ preserved e…       ┆                  ┆                    ┆   ┆                   ┆                 ┆                  ┆                   │
# │ 4                  ┆ hfpef              ┆ 1                ┆ 0                  ┆ … ┆ 1                 ┆ 1               ┆ 1                ┆ 1                 │
# │ 5                  ┆ hyponatremia       ┆ 1                ┆ 1                  ┆ … ┆ 1                 ┆ 1               ┆ 1                ┆ 1                 │
# └────────────────────┴────────────────────┴──────────────────┴────────────────────┴───┴───────────────────┴─────────────────┴──────────────────┴───────────────────┘

# search_term_to_note_groups_id
# search_term
# admission_notes_group
# communication_encounter_notes_group
# discharge_summary_notes_group
# ecg_impression_notes_group
# emergency_department_notes_group
# inpatient_notes_group
# outpatient_notes_group
# problem_list_notes_group
