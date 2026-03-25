import os
from typing import Generator, Any, Iterator, List
import spacy
from spacy.tokens import Doc
from medspacy.ner import TargetRule

from common.instance_logr_mixin import InstanceLogrMixin
from common.worker_mixin import WorkerMixin
from nlp_method.data.map_search_term_to_note_group import MapSearchTermToNoteGroup
from nlp_method.notes import TARGET_ENTITY_LABEL


class NLPProcessor(WorkerMixin, InstanceLogrMixin):
    """
    NLPProcessor is responsible for processing clinical notes using a spaCy NLP pipeline.
    It integrates with the medSpaCy library to perform target matching and context analysis.
    The processor takes in a generator of note texts and additional context, processes the
    notes through the NLP pipeline, and yields processed Doc objects along with their context.
    """

    def __init__(self, term_to_note_grp_map: MapSearchTermToNoteGroup, *args, **kwargs):

        model = os.getenv("SPACY_MODEL", None)
        if model is None:
            raise ValueError("SPACY_MODEL environment variable not defined.")
        self._model: str = model
        self._map: MapSearchTermToNoteGroup = term_to_note_grp_map
        nlp = spacy.load(self._model)
        nlp.add_pipe("medspacy_target_matcher")
        target_matcher = nlp.get_pipe("medspacy_target_matcher")
        target_matcher.add(  # type: ignore
            [
                TargetRule(search_term.lower(), TARGET_ENTITY_LABEL)
                for search_term in term_to_note_grp_map.search_terms
            ]
        )
        nlp.add_pipe("medspacy_context")  # This adds clinical negation
        self._nlp = nlp
        super().__init__(*args, **kwargs)

    @property
    def pipeline_components(self) -> List[str]:
        return [str(x) for x in self._nlp.pipeline]

    def __call__(
        self, notes_and_data: Generator[tuple[str, tuple[Any, ...]], Any, None]
    ) -> Iterator[tuple[Doc, tuple[Any, ...]]]:
        self.log("info", "Processing notes...")

        def note_data_iter():
            for note_text, additional_vars in notes_and_data:
                yield note_text.lower().strip(), additional_vars

        # Call to MedSpaCy pipeline with note text and additional context
        for doc, context in self._nlp.pipe(
            note_data_iter(), disable=["ner"], as_tuples=True
        ):
            yield doc, context

        self.log("info", "Notes processed.")
