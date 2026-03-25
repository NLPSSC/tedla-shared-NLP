import os
from typing import Dict
from loguru import logger


TABLE_SCHEMA: Dict[str, str] = {
    "note_id": "int64",
    "batch_group": "int64",
    "patient_id": "int64",
    "window_text": "str",
    "note_date": "date",
    "search_term": "str",
    "problem_list_notes_group": "bool",
    "outpatient_notes_group": "bool",
    "communication_encounter_notes_group": "bool",
    "inpatient_notes_group": "bool",
    "admission_notes_group": "bool",
    "emergency_department_notes_group": "bool",
    "ecg_impression_notes_group": "bool",
    "discharge_summary_notes_group": "bool",
    "is_patient_communication": "bool",
    "is_note_within_visit": "bool",
    "is_negated": "bool",
    "window_start_char_offset": "int64",
    "window_end_char_offset": "int64",
    "entity_start_offset": "int64",
    "entity_end_offset": "int64",
}

RESULTS_TABLE_NAME = os.getenv("RESULTS_TABLE_NAME", None)
if RESULTS_TABLE_NAME is None:
    logger.warning(
        "RESULTS_TABLE_NAME environment variable is not defined; defaulting to 'results'"
    )
    RESULTS_TABLE_NAME = "results"
if len(RESULTS_TABLE_NAME) < 5:
    raise ValueError("RESULTS_TABLE_NAME must be at least 5 characters long.")

__all__ = ["TABLE_SCHEMA", "RESULTS_TABLE_NAME"]
