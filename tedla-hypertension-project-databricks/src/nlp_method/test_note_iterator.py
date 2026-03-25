from time import time
from dotenv import load_dotenv

load_dotenv("/home/westerd/_/research_projects/tedla-hypertension/src/nlp_method/.env")
from datasources.data.note_data import NoteData
from nlp_method.notes.notes_iterator import NotesIterator


if __name__ == "__main__":
    note_data: NoteData = NoteData(
        filter_to_datasets=None  # ["note_data_2010_to_2011_parquet"]
    )
    for notes_df in NotesIterator(note_data, 1):
        start_time = time()
        print(f"{len(notes_df)} @ {(time() - start_time)} secs")
