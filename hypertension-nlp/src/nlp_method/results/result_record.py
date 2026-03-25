from dataclasses import dataclass
from datetime import date


@dataclass
class BaseData:
    batch_group: int  # the batch in which this was run
    note_id: str  # the note id from the RD
    person_id: int  # the person id from the RD
    note_date: date  # the date of the note
    problem_list_notes_group: bool
    outpatient_notes_group: bool
    communication_encounter_notes_group: bool
    inpatient_notes_group: bool
    admission_notes_group: bool
    emergency_department_notes_group: bool
    ecg_impression_notes_group: bool
    discharge_summary_notes_group: bool
    is_patient_communication: (
        bool  # additional flag indicating whether this is a patient communication
    )
    is_note_within_visit: bool  # the relative position of the note within the visit (e.g., True if the note is within the visit, False if it is outside the visit)

    @staticmethod
    def columns() -> list[str]:
        return [field.name for field in BaseData.__dataclass_fields__.values()]


@dataclass
class SourceData(BaseData):
    note_text: str  # the full text of the note, which will be processed by the NLP pipeline to extract entities and context

    @staticmethod
    def columns() -> list[str]:
        return [field.name for field in SourceData.__dataclass_fields__.values()]


@dataclass
class ResultRecord(BaseData):
    search_term: str  # the search term that was matched
    window_text: str  # the text of the window around the entity mention
    is_negated: bool  # whether the entity mention is negated according to medspacy's context component
    window_start_char_offset: int  # text windows character offset start
    window_end_char_offset: int  # text windows character offset end
    entity_start_offset: int  # entity character offset start
    entity_end_offset: int  # entity character offset end

    @staticmethod
    def columns() -> list[str]:
        return [field.name for field in ResultRecord.__dataclass_fields__.values()]

    def __repr__(self) -> str:
        return f"ResultRecord(note_id={self.note_id}, search_term='{self.search_term}')"
