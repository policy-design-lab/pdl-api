from app.models.db import db


class Practice(db.Model):
    __tablename__ = 'practices'
    __table_args__ = {"schema": "pdl"}

    code = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    display_name = db.Column(db.String())
    source = db.Column(db.String())

    def __init__(self, code, name, display_name, source):
        self.code = code
        self.name = name
        self.display_name = display_name
        self.source = source

    def __repr__(self):
        return 'Practice(code=%s, name=%s, display_name=%s, source=%s)' % (
            self.code, self.name, self.display_name, self.source)
