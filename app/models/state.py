from app.models.db import db


class State(db.Model):
    __tablename__ = 'states'

    state_code = db.Column(db.String(), primary_key=True)
    state_name = db.Column(db.String())

    def __init__(self, state_code, state_name):
        self.state_code = state_code
        self.state_name = state_name

    def __repr__(self):
        return 'Summary(state_code=%s, state_name=%s)' % (self.state_code, self.state_name)

    def json(self):
        return {'title': self.title, 'state': self.state_name}