from app.models.db import db


class Subtitle(db.Model):
    __tablename__ = 'subtitles'
    __table_args__ = {"schema": "pdl"}

    id = db.Column(db.Integer, primary_key=True)
    title_id = db.Column(db.Integer)
    name = db.Column(db.String())

    def __init__(self, title_id, name):
        self.title_id = title_id
        self.name = name

    def __repr__(self):
        return 'Subtitles(title_id=%s, name=%s)' % (self.title_id, self.name)

    def json(self):
        return {'name': self.name, 'title_id': self.title_id}
