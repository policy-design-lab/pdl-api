from app.models.db import db


class Summary(db.Model):
    __tablename__ = 'summary'
    __table_args__ = {"schema": "public"}

    summary_code = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    state = db.Column(db.String())
    fiscal_year = db.Column(db.Integer())
    amount = db.Column(db.Integer())

    def __init__(self, title, state, fiscal_year, amount):
        self.title = title
        self.state = state
        self.fiscal_year = fiscal_year
        self.amount = amount

    def __repr__(self):
        return 'Summary(title=%s, state=%s, fiscal_year=%d, amount=%s)' \
               % (self.title, self.state, self.fiscal_year, self.amount)

    def json(self):
        return {'title': self.title, 'state': self.state, 'fiscal_year': self.fiscal_year, 'amount': self.amount}
