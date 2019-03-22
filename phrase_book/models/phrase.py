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
        self.id = uuid4()
        self.book_id = book_id
        self.source_phrase = source_phrase
        self.source_phrase_language = 'en'
        self.translations: Dict = {}

    def to_json(self):
        property_names = Phrase.__table__.columns.keys()
        configs = {}
        for prop in [p for p in property_names]:
            value = getattr(self, prop)
            configs[prop] = value

        return configs
