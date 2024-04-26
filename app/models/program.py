from app.models.db import db


class Program(db.Model):
    __tablename__ = 'programs'
    __table_args__ = {"schema": "pdl"}

    id = db.Column(db.Integer, primary_key=True)
    title_id = db.Column(db.Integer)
    subtitle_id = db.Column(db.Integer)
    name = db.Column(db.String())

    def __init__(self, title_id, subtitle_id, name):
        self.title_id = title_id
        self.subtitle_id = subtitle_id
        self.name = name

    def __repr__(self):
        return 'Programs(title_id=%s, subtitle_id=%s, name=%s)' % (self.title_id, self.subtitle_id, self.name)

    def json(self):
        return {'title_id': self.title_id, 'subtitle_id': self.subtitle_id, 'name': self.name}
