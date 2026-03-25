from nlp_method.data.map_search_term_to_note_group import MapSearchTermToNoteGroup
from nlp_method.nlp.nlp_method import NLPProcessor
from nlp_method.notes.note_batch_processor import NoteBatchProcessor
from nlp_method.results.result_writer import ResultWriter
from loguru import logger


def initialize_nlp_processor(worker_id: int) -> NoteBatchProcessor:
    logger.info("Initializing NLP processor for worker #{}...", worker_id)
    map_search_term_to_note_group = MapSearchTermToNoteGroup()
    nlp_processor = NLPProcessor(map_search_term_to_note_group, worker_id=worker_id)
    result_writer = ResultWriter(worker_id=worker_id)
    nlp_batch_processor = NoteBatchProcessor(
        result_writer, nlp_processor, map_search_term_to_note_group, worker_id=worker_id
    )
    logger.info("NLP processor for worker #{} initialized.", worker_id)

    return nlp_batch_processor
