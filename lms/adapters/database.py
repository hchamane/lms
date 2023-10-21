from dataclasses import dataclass
from datetime import datetime
from typing import Any

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer

db = SQLAlchemy()


@dataclass
class BaseMixin(object):
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def find_by(cls, **kwargs) -> Any | None:
        filters = cls._filters(kwargs)
        return db.session.execute(db.select(cls).where(*filters)).scalars().first()

    @classmethod
    def _filters(cls, kwargs):
        return [getattr(cls, attr) == kwargs[attr] for attr in kwargs]
