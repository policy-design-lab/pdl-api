
from app.models.db import db


class County(db.Model):
    __tablename__ = 'counties'
    __table_args__ = {"schema": "pdl"}

    fips_code = db.Column(db.String(), primary_key=True)
    state_code = db.Column(db.String())
    name = db.Column(db.String())
    remarks = db.Column(db.String())

    def __init__(self, fips_code, state_code, name, remarks=None):
        self.fips_code = fips_code
        self.state_code = state_code
        self.name = name
        self.remarks = remarks

    def __repr__(self):
        return 'County(fips_code=%s, state_code=%s, name=%s)' % (self.fips_code, self.state_code, self.name)

    def json(self):
        return {
            'fips_code': self.fips_code,
            'state_code': self.state_code,
            'name': self.name,
            'remarks': self.remarks
        }