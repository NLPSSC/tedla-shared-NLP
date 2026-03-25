from typing import List
import pandas as pd
from datasources.data.note_group_to_term import NoteGroupToTermMap
from loguru import logger


class MapSearchTermToNoteGroup:

    JOIN_COLS: List[str] = [
        "notes_admissions",
        "notes_communication_encounter",
        "notes_discharge_summary",
        "notes_ecg_impression",
        "notes_emergency_department",
        "notes_inpatient",
        "notes_outpatient",
        "notes_problem_lists",
    ]

    def __init__(self):
        logger.info("Initializing MapSearchTermToNoteGroup...")
        self._note_group_to_term_map = NoteGroupToTermMap().get()
        self._search_terms_series: pd.Series = self._note_group_to_term_map[
            "search_term"
        ]
        assert len(self._search_terms_series) == 116
        self._search_terms: List[str] = list(
            str(x) for x in self._note_group_to_term_map["search_term"].to_list()
        )
        assert len(self._search_terms) == 116
        logger.info("MapSearchTermToNoteGroup initialized.")

    @property
    def search_terms(self) -> List[str]:
        return self._search_terms

    def search_terms_series(self) -> pd.Series:
        return self._search_terms_series

    def get_search_terms_by_groups(self, note_row: pd.Series) -> set[str]:
        logger.debug("Getting search terms for note with id {}...", note_row["note_id"])
        note_groups: list[str] = NoteGroupToTermMap.note_groups()

        search_terms: set[str] = {
            x
            for ng in note_groups
            if note_row[ng] == 1
            for x in list(self._note_group_to_term_map[ng])
        }
        logger.debug(
            "Search terms for note with id {}: {}", note_row["note_id"], search_terms
        )

        return search_terms
