from app.models.db import db


class StateCode(db.Model):
    __tablename__ = 'statecodes'

    state_code = db.Column(db.String(), primary_key=True)
    state_name = db.Column(db.String())

    def __init__(self, state_name, state_code):
        self.state_code = state_code
        self.state_name = state_name

    def __repr__(self):
        return 'Summary(state_name=%s, state_code=%s)' % (self.state_name, self.state_code)

    def json(self):
        return {'state name': self.state_name, 'state code': self.state_code}
