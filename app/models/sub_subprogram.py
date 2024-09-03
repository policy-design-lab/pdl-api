from app.models.db import db


class SubSubProgram(db.Model):
    __tablename__ = 'sub_sub_programs'
    __table_args__ = {"schema": "pdl"}

    id = db.Column(db.Integer, primary_key=True)
    sub_program_id = db.Column(db.Integer)
    name = db.Column(db.String())

    def __init__(self, sub_program_id, name):
        self.sub_program_id = sub_program_id
        self.name = name

    def __repr__(self):
        return 'SubSubPrograms(sub_program_id=%s, name=%s)' % (self.sub_program_id, self.name)

    def json(self):
        return {'sub_program_id': self.sub_program_id, 'name': self.name}
