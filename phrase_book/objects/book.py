from typing import List
from uuid import uuid4

from phrase_book.objects.phrase import Phrase


class Book:
    def __init__(self, phrases: List[Phrase] = []):
        self._book_id: str = str(uuid4())
        self._phrases: list[Phrase] = []
        self.add_phrases(phrases)

    def add_phrase(self, phrase: Phrase):
        self.phrases.append(phrase)

    def add_phrases(self, phrases: List[Phrase]):
        self.phrases.extend(phrases)

    def to_json(self):
        property_names = [p for p in dir(Book) if isinstance(getattr(Book, p), property)]
        configs = {}
        for prop in [p for p in property_names if p.upper() not in []]:
            value = getattr(self, prop)
            configs[prop] = value

        return configs

    # Properties

    @property
    def id(self) -> str:
        return self._book_id

    @property
    def phrases(self) -> List[Phrase]:
        return self._phrases

    @phrases.setter
    def phrases(self, value):
        self._phrases = value
