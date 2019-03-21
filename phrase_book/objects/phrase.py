import logging
from typing import Dict
from uuid import uuid4

logger = logging.getLogger(__name__)


class Phrase:
    def __init__(self, source_phrase: str, book_id: str):
        self._phrase_id: str = str(uuid4())
        self._book_id = book_id
        self._source_phrase = source_phrase
        self._source_phrase_language = None
        self._translations: Dict = {}

    def to_json(self):
        property_names = [p for p in dir(Phrase) if isinstance(getattr(Phrase, p), property)]
        configs = {}
        for prop in [p for p in property_names]:
            value = getattr(self, prop)
            configs[prop] = value

        return configs

    # Properties
    @property
    def id(self) -> str:
        return self._phrase_id

    @property
    def book_id(self) -> str:
        return self._book_id

    @book_id.setter
    def book_id(self, value):
        self._book_id = value

    @property
    def source_phrase(self) -> str:
        return self._source_phrase

    @property
    def source_phrase_language(self) -> str:
        return self._source_phrase_language

    @property
    def translations(self) -> Dict:
        return self._translations
