from app.models.db import db


class Title(db.Model):
    __tablename__ = 'titles'
    __table_args__ = {"schema": "pdl"}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return 'Titles(name=%s, description=%s)' % (self.name, self.description)

    def json(self):
        return {'name': self.name, 'description': self.description}
