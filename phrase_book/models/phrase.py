import logging
from typing import Dict
from uuid import uuid4

from google.cloud import translate
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.hybrid import hybrid_property

from phrase_book import db, app
from phrase_book.models.metadata_mixin import MetaDataMixIn
from phrase_book.settings.constants import SUPPORTED_LANGUAGES

logger = logging.getLogger(__name__)

if not app.testing:
    translate_client = translate.Client()


class Phrase(MetaDataMixIn, db.Model):
    __tablename__ = 'phrases'

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4, nullable=False)
    book_id = db.Column(UUID(as_uuid=True), db.ForeignKey('books.id'), nullable=False)
    _source_phrase = db.Column('source_phrase', db.String, nullable=False)
    source_phrase_language = db.Column(db.String, nullable=False)
    translations = db.Column(JSONB, nullable=False)

    def __init__(self, source_phrase: str, book_id: str):
        self.id = uuid4()
        self.book_id = book_id
        self.source_phrase_language = None
        self.translations: Dict = {}
        self.source_phrase = source_phrase

    def to_json(self):
        property_names = Phrase.__table__.columns.keys()
        configs = {}
        for prop in [p for p in property_names]:
            value = getattr(self, prop)
            configs[prop] = value

        return configs

    @hybrid_property
    def source_phrase(self) -> str:
        return self._source_phrase

    @source_phrase.setter
    def source_phrase(self, value):
        self._source_phrase = value
        self._translate_source_phrase()

    def _translate_source_phrase(self):
        self.translations = {}
        for language in SUPPORTED_LANGUAGES:
            translation: Dict = translate_client.translate(self.source_phrase, target_language=language)
            self.source_phrase_language = translation['detectedSourceLanguage']
            self.translations[language] = translation['translatedText']
