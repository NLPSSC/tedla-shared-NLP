import sys
import pytest
from spacy.tokens import Doc, Span
from spacy.vocab import Vocab


sys.path.insert(0, "src")


ENGLISH_PARAGRAPHS_WITH_500_TOKENS_AND_SENTENCES = """
The sun rose quietly over the city. Birds began to sing in the trees. People started their daily routines. Some rushed to catch the morning train. Others enjoyed a slow breakfast at home. The streets filled with cars and bicycles. Children laughed as they walked to school. The air was fresh and cool. Shops opened their doors to customers. The city buzzed with energy.
In the afternoon, clouds gathered above the skyline. Rain threatened but did not fall. Workers took breaks in nearby parks. Friends met for coffee and conversation. Laughter echoed from busy cafes. A gentle breeze moved through the open windows. Books were read in quiet corners. Artists painted scenes of daily life. The hours passed with steady rhythm. Evening approached with golden light.
Night settled softly over the neighborhood. Lights glowed in windows and on streets. Families shared meals and stories. Pets curled up in warm places. Music played from distant houses. The world slowed down and grew quiet. Stars appeared in the dark sky. Dreams began to form in sleeping minds. Tomorrow waited just beyond the horizon. Peace filled the silent night.
"""

from nlp_method.notes import TARGET_ENTITY_LABEL


@pytest.fixture(scope="session")
def doc() -> Doc:
    return Doc(
        Vocab(),
        words=[
            str(x)
            for x in ENGLISH_PARAGRAPHS_WITH_500_TOKENS_AND_SENTENCES.strip().split()
        ],
    )


def test_can_get_window_offset(doc: Doc):
    from nlp_method.notes.note_batch_processor import _get_window_data

    anchor_entity = Span(doc, 1, 2, label=TARGET_ENTITY_LABEL)
    doc.ents = [anchor_entity]
    start, end = _get_window_data(anchor_entity, doc)
    assert start == 0
    assert end == len(doc[0].text)


# These test cases evaluate the method `_get_window_char_offsets` in `NoteBatchProcessor`
# to ensure it correctly calculates the character offsets for a window of tokens around
# an entity span, even when the sentence has varying numbers of tokens.

# Test Cases
# 1) Text with >= 20 tokens
#   a) Token on lhs where there are fewer than WINDOW_SIZE tokens before the token in the text
#   b) Token on rhs where there are fewer than WINDOW_SIZE tokens after the token in the text
#   c) Token where there are at least WINDOW_SIZE to the left and right of the token in the text
# 2) Text with 10 to 20 tokens
#   a) Token on lhs where there are fewer than WINDOW_SIZE tokens before the token in the text
#   b) Token on rhs where there are fewer than WINDOW_SIZE tokens after the token in the text
#   c) Token where there are
# 3) Text with fewer than 10 tokens
# 4) Text with one token
