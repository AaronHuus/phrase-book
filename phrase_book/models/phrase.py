import logging
from typing import Dict
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID, JSONB

from phrase_book import db
from phrase_book.models.metadata_mixin import MetaDataMixIn

logger = logging.getLogger(__name__)


class Phrase(MetaDataMixIn, db.Model):
    __tablename__ = 'phrases'

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4, nullable=False)
    book_id = db.Column(UUID(as_uuid=True), db.ForeignKey('books.id'), nullable=False)
    source_phrase = db.Column(db.String, nullable=False)
    source_phrase_language = db.Column(db.String, nullable=False)
    translations = db.Column(JSONB, nullable=False)

    def __init__(self, source_phrase: str, book_id: str):
        self._phrase_id = uuid4()
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
    # @property
    # def id(self) -> str:
    #     return str(self._phrase_id)
    #
    # @property
    # def book_id(self) -> str:
    #     return self._book_id
    #
    # @book_id.setter
    # def book_id(self, value):
    #     self._book_id = value
    #
    # @property
    # def source_phrase(self) -> str:
    #     return self._source_phrase
    #
    # @property
    # def source_phrase_language(self) -> str:
    #     return self._source_phrase_language
    #
    # @property
    # def translations(self) -> Dict:
    #     return self._translations
