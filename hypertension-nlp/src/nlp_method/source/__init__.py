import os

COHORT_NOTE_DATA_TABLE = os.getenv("COHORT_NOTE_DATA_TABLE", None)
if COHORT_NOTE_DATA_TABLE is None:
    raise ValueError("COHORT_NOTE_DATA_TABLE environment variable is not set")

NOTE_ID_TO_NOTE_GROUPS_TABLE = os.getenv("NOTE_ID_TO_NOTE_GROUPS_TABLE", None)
if NOTE_ID_TO_NOTE_GROUPS_TABLE is None:
    raise ValueError("NOTE_ID_TO_NOTE_GROUPS_TABLE environment variable is not set")

COHORT_NOTE_VISIT_DETAILS = os.getenv("COHORT_NOTE_VISIT_DETAILS", None)
if COHORT_NOTE_VISIT_DETAILS is None:
    raise ValueError("COHORT_NOTE_VISIT_DETAILS environment variable is not set")


RESULTS_TABLE = os.getenv("RESULTS_TABLE", None)
if RESULTS_TABLE is None:
    raise ValueError("RESULTS_TABLE environment variable is not set")

__all__ = [
    "COHORT_NOTE_DATA_TABLE",
    "NOTE_ID_TO_NOTE_GROUPS_TABLE",
    "RESULTS_TABLE",
    "COHORT_NOTE_VISIT_DETAILS",
]
