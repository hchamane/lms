from dataclasses import dataclass

from lms.adapters import BaseMixin, db


@dataclass
class FeatureSwitch(BaseMixin, db.Model):
    __tablename__ = "feature_switches"

    name: str = db.Column("name", db.String(255), nullable=False)
    active: int = db.Column("active", db.Integer, nullable=False, default=0)

    def __init__(self, name: str, active: int = 0) -> None:
        self.name = name
        self.active = active

    @classmethod
    def create(cls, name: str, active: int = 0) -> "FeatureSwitch":
        feature_switch = cls(name=name, active=active)
        db.session.add(feature_switch)
        db.session.commit()
        return feature_switch

    def set_value(self, active: int) -> None:
        self.active = active
        db.session.commit()
