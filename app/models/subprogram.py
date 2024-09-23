from app.models.db import db


class SubProgram(db.Model):
    __tablename__ = 'sub_programs'
    __table_args__ = {"schema": "pdl"}

    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer)
    name = db.Column(db.String())

    def __init__(self, program_id, name):
        self.program_id = program_id
        self.name = name

    def __repr__(self):
        return 'SubPrograms(program_id=%s, name=%s)' % (self.program_id, self.name)

    def json(self):
        return {'program_id': self.program_id, 'name': self.name}
