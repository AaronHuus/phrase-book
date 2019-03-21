from typing import List
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from phrase_book import db

from phrase_book.models.phrase import Phrase
from phrase_book.models.metadata_mixin import MetaDataMixIn


class Book(MetaDataMixIn, db.Model):
    __tablename__ = 'books'

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4, nullable=False)
    display_name = db.Column(db.String, nullable=False)
    phrases: List[Phrase] = db.relationship("Phrase", backref='books')

    def __init__(self, display_name: str):
        self.id = uuid4()
        self.display_name: str = display_name

    def to_json(self):
        property_names = Book.__table__.columns.keys()
        configs = {}
        for prop in [p for p in property_names if p.upper() not in []]:
            value = getattr(self, prop)
            configs[prop] = value

        return configs