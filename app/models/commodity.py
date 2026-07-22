from app.models.db import db

class Commodity(db.Model):
    __tablename__ = 'commodities'
    __table_args__ = {"schema": "pdl"}

    code = db.Column(db.SmallInteger, primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    abbreviation = db.Column(db.String())

    def __init__(self, code, name, abbreviation=None):
        self.code = code
        self.name = name
        self.abbreviation = abbreviation

    def json(self):
        return {
            'code': self.code,
            'name': self.name,
            'abbreviation': self.abbreviation
        }