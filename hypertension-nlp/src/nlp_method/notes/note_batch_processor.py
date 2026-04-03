import time
from pathlib import Path
from typing import Any, Generator, List

import pandas as pd
from common.instance_logr_mixin import InstanceLogrMixin
from common.worker_mixin import WorkerMixin
from loguru import logger
from nlp_method.data.map_search_term_to_note_group import \
    MapSearchTermToNoteGroup
from nlp_method.nlp.nlp_method import NLPProcessor
from nlp_method.notes import TARGET_ENTITY_LABEL, WINDOW_SIZE
from nlp_method.results.result_record import BaseData, ResultRecord
from nlp_method.results.writer_base import WriterBase
from spacy.tokens import Doc
from spacy.tokens.span import Span
from tqdm import tqdm


class NoteBatchProcessor(WorkerMixin, InstanceLogrMixin):

    def __init__(
        self,
        writer: WriterBase,
        nlp_processor: NLPProcessor,
        map_search_term_to_note_group: MapSearchTermToNoteGroup,
        *args,
        **kwargs,
    ) -> None:
        logger.info("Initializing NoteBatchProcessor...")
        self._writer: WriterBase = writer
        self._nlp_processor: NLPProcessor = nlp_processor
        self._map_search_term_to_note_group: MapSearchTermToNoteGroup = (
            map_search_term_to_note_group
        )

        super().__init__(*args, **kwargs)
        logger.info("NoteBatchProcessor initialized.")

    def __call__(self, note_batch_df: pd.DataFrame):

        self.log("info", "Processing batch of {} notes...", len(note_batch_df))

        columns = [x for x in note_batch_df.columns if x != "note_text"]
        note_texts = note_batch_df["note_text"].tolist()
        note_contexts = note_batch_df[columns].to_dict("records")

        def note_iterator() -> Generator[tuple[str, tuple[Any, ...]], Any, None]:
            # Create a generator that yields tuples of (note_text, additional_vars) for each note in the batch.
            for note_text, other_values in zip(note_texts, note_contexts):
                additional_vars = (other_values,)
                yield note_text, additional_vars

        doc: Doc
        start_time = time.time()
        all_results: List[ResultRecord] = []
        with tqdm(total=len(note_batch_df), desc=f"Worker #{self.worker_id} processing notes") as pbar:
            # Process the notes through the NLP pipeline and create result records for each identified entity of interest.
            for doc, context in self._nlp_processor(note_iterator()):

                records: List[ResultRecord] = self._assemble_result_records(doc, context)
                if len(records) > 0:
                    all_results.extend(records)
                pbar.update(1)

            self._writer(all_results)

            self.log(
                "info", "Finished processing notes in {} seconds", time.time() - start_time
            )

    def get_results_db_path(self) -> Path:
        return self._writer.get_path()

    def _assemble_result_records(
        self, doc: Doc, context: tuple[Any, ...]
    ) -> List[ResultRecord]:

        base_data = BaseData(**context[0])

        # Find entities in the document that match the TARGET_ENTITY_LABEL, which indicates they are 
        # symptoms of interest based on the search terms.
        symptoms_of_interest: list[Span] = [
            ent for ent in doc.ents if ent.label_ == TARGET_ENTITY_LABEL
        ]

        records: List[ResultRecord] = []

        # Group the identified symptoms of interest by their text to facilitate matching with search terms.
        entities_by_text: dict[str, list[Span]] = {}
        for symptom in symptoms_of_interest:
            entities_by_text.setdefault(symptom.text, []).append(symptom)


        # Create ResultRecord objects for each identified symptom of interest that matches the search terms,
        # including context such as negation status and character offsets.
        entities_of_interest: List[Span] = [
            soi
            for st in self._map_search_term_to_note_group.search_terms
            for soi in entities_by_text.get(st, [])
        ]

        # Review each identified entity of interest and create a ResultRecord for it, including the context
        # of the note and the entity.
        for entity_of_interest in entities_of_interest:

            # A found search term 
            search_term: str = entity_of_interest.text

            # Calculate the window of text around the identified entity to provide context for the result record.
            (window_start, window_end), window_text = self._get_window_data(
                entity_of_interest, doc
            )

            # Double-check that the term actually exists within the window text
            if search_term not in window_text:
                raise RuntimeError(
                    f"Search term '{search_term}' not found in window text: '{window_text}'"
                )

            from datetime import date

            import pandas as pd
            lb_date = date(2018, 1, 1)
            if search_term.lower().strip() in ['heart failure with reduced ejection fraction','hfref','heart failure with preserved ejection fraction','hfpef']:
                lb_date = date(2010, 1, 1)

            if base_data.note_date < pd.Timestamp(lb_date):
                logger.debug('test')
                pass

            is_patient_communication: bool = base_data.is_patient_communication
            is_note_within_visit: bool = base_data.is_note_within_visit

            result_record = ResultRecord(
                    batch_group=base_data.batch_group,
                    note_id=base_data.note_id,
                    person_id=base_data.person_id,
                    window_text=window_text,
                    note_date=base_data.note_date,
                    problem_list_notes_group=base_data.problem_list_notes_group,
                    outpatient_notes_group=base_data.outpatient_notes_group,
                    communication_encounter_notes_group=base_data.communication_encounter_notes_group,
                    inpatient_notes_group=base_data.inpatient_notes_group,
                    admission_notes_group=base_data.admission_notes_group,
                    emergency_department_notes_group=base_data.emergency_department_notes_group,
                    ecg_impression_notes_group=base_data.ecg_impression_notes_group,
                    discharge_summary_notes_group=base_data.discharge_summary_notes_group,
                    search_term=search_term,
                    is_patient_communication=is_patient_communication,
                    is_note_within_visit=is_note_within_visit,
                    is_negated=entity_of_interest._.is_negated,
                    window_start_char_offset=window_start,
                    window_end_char_offset=window_end,
                    entity_start_offset=entity_of_interest.start_char,
                    entity_end_offset=entity_of_interest.end_char,
                )
    
            records.append(
                result_record
            )
        return records

    def _get_window_data(self, ent: Span, doc: Doc) -> tuple[tuple[int, int], str]:
        """
        Calculate the character offsets for a window of tokens around a given entity span within a spaCy Doc.
        The window is defined by extending WINDOW_SIZE tokens before and after the entity span.
        The function returns the starting and ending character offsets of this window in the document text.
        Args:
            ent (Span): The spaCy Span representing the entity within the document.
            doc (Doc): The spaCy Doc object containing the text and tokens.
        Returns:
            tuple[int, int]: A tuple containing the start and end character offsets of the window.
        """
        try:
            tokens_before = doc[: ent.start]
            tokens_after = doc[ent.end :]
            window_to_left = tokens_before[-WINDOW_SIZE:]
            window_to_right = tokens_after[:WINDOW_SIZE]
            first_token_left_left = (
                window_to_left[0] if len(window_to_left) > 0 else None
            )
            last_token_to_right = (
                window_to_right[-1] if len(window_to_right) > 0 else None
            )
            window_start_offset = (
                first_token_left_left.idx if first_token_left_left is not None else 0
            )
            window_end_offset = (
                (last_token_to_right.idx + len(last_token_to_right.text))
                if last_token_to_right is not None
                else len(doc.text)
            )
            window_text = doc.text[window_start_offset:window_end_offset]

            return (window_start_offset, window_end_offset), window_text
        except Exception as e:
            logger.error(
                "Error calculating window data for entity '{}': {}",
                ent.text,
                e,
            )
            raise
