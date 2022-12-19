from app.models.db import db


class State(db.Model):
    __tablename__ = 'states'

    state_fips = db.Column(db.String(), primary_key=True)
    state_code = db.Column(db.String())

    def __init__(self, state_fips, state_code):
        self.state_code = state_code
        self.state_fips = state_fips

    def __repr__(self):
        return 'Summary(state_fips=%s, state_code=%s)' % (self.state_fips, self.state_code)

    def json(self):
        return {'state fips': self.state_fips, 'state code': self.state_code}