from sqlalchemy import func

from phrase_book import db


class MetaDataMixIn:
    created_on = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    created_by = db.Column(db.String, default='dummyUser', nullable=False)
    updated_on = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now())
    updated_by = db.Column(db.String, default='dummyUser', nullable=False)
