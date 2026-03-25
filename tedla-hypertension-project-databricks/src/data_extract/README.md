# Implementation Notes

This code represents a transcription of an implementation built on Azure databricks.  As such, your own implementation will likely vary as it pertains to accessing data.  The code has been re-written to accomodate local database access (e.g. MSSQL, Postgresql, MySql, etc.).  The NLP method itself remains the same as used in databricks, but the additional work done to create data flow is provided for reference to use in constructing your own solution.

## Setup

This was implemented with Python 3.11.14.  From within the virtual environment, you can install the requirements using

```shell
python -m pip install --upgrade -r requirements.txt -c pip_constraints.txt
```

## Workflow

- Define MRNs and with id for cohort.
- Define notes associated with each patient.  There needs to be a batch group number (monotoniclly increasing value) to permit batching notes through the NLP method (see COHORT_NOTE_DATA_TABLE below).
- Define each of the note groups as specified within the NLP method specification.
- For each note, create a bitmap of note group relationships (see NOTE_ID_TO_NOTE_GROUPS_TABLE below).
- Within the `__main__.py`, 
  - the `notes_iterator()` method will iterate over the notes for the cohort, yield a pandas dataset,
  - the `NoteBatchProcessor` instance will then
    - iterate over each note in the batch,
    - invoke the NLP method, and
    - write the result to the `RESULTS_TABLE` table (defined in .env)

## Required Source Tables

The following tables will need to be defined per the method specification documents.  Define the table name with the .env file.

### NOTE_ID_TO_NOTE_GROUPS_TABLE
  - note_id
  - notes_problem_lists - is member of class True/False
  - notes_outpatient - is member of class True/False
  - notes_inpatient - is member of class True/False
  - notes_emergency_department - is member of class True/False
  - notes_ecg_impression - is member of class True/False
  - notes_discharge_summary - is member of class True/False
  - notes_communication_encounter - is member of class True/False
  - notes_admissions - is member of class True/False

### COHORT_NOTE_DATA_TABLE
  - note_id - the unique_note_id
  - batch_group - the batch group (i.e., 1000 notes per group, used for processing)
  - note_text - the text of the note



