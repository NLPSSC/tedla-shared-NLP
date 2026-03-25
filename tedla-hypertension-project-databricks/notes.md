"c:\Users\westerd\.vscode\extensions\databricks.databricks-2.10.3-win32-x64\bin\databricks.exe" fs --profile dev cp -r dbfs:/tmp/table_export/default.cohort_note_data "Z:\_\active\nlpssc\Tedla - VUMC\tedla-hypertension-project-databricks\.data" 

## Data Needed for Run

note_id
person_id
note_text
visit_start_date
visit_end_date


## Table Created For Results

```sql
CREATE TABLE IF NOT EXISTS results 
(
    result_id INTEGER PRIMARY KEY AUTOINCREMENT
    , note_id INTEGER
    , batch_group INTEGER
    , person_id INTEGER
    , window_text TEXT
    , note_date DATE
    , search_term TEXT
    , problem_list_notes_group BOOLEAN
    , outpatient_notes_group BOOLEAN
    , communication_encounter_notes_group BOOLEAN
    , inpatient_notes_group BOOLEAN
    , admission_notes_group BOOLEAN
    , emergency_department_notes_group BOOLEAN
    , ecg_impression_notes_group BOOLEAN
    , discharge_summary_notes_group BOOLEAN
    , is_patient_communication BOOLEAN
    , is_note_within_visit BOOLEAN
    , is_negated BOOLEAN
    , window_start_char_offset INTEGER
    , window_end_char_offset INTEGER
    , entity_start_offset INTEGER
    , entity_end_offset INTEGER
)
```