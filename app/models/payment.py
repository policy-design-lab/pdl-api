from app.models.db import db


class Payment(db.Model):
    __tablename__ = 'payments'
    __table_args__ = {"schema": "pdl"}

    id = db.Column(db.Integer, primary_key=True)
    title_id = db.Column(db.Integer)
    subtitle_id = db.Column(db.Integer)
    program_id = db.Column(db.Integer)
    sub_program_id = db.Column(db.Integer)
    state_code = db.Column(db.String())
    year = db.Column(db.Integer)
    payment = db.Column(db.Float)
    recipient_count = db.Column(db.Integer)
    base_acres = db.Column(db.Float)

    def __init__(self, title_id, subtitle_id, program_id, sub_program_id, state_code, year, payment, recipient_count, base_acres):
        self.title_id = title_id
        self.subtitle_id = subtitle_id
        self.program_id = program_id
        self.sub_program_id = sub_program_id
        self.state_code = state_code
        self.year = year
        self.payment = payment
        self.recipient_count = recipient_count
        self.base_acres = base_acres

    def __repr__(self):
        return 'Payments(title_id=%s, subtitle_id=%s, program_id=%s, sub_program_id=%s, state_code=%s, year=%s, payment=%s, recipient_count=%s, base_acres=%s)' % (
            self.title_id, self.subtitle_id, self.program_id, self.sub_program_id, self.state_code, self.year, self.payment, self.recipient_count, self.base_acres)

    def json(self):
        return {'title_id': self.title_id, 'subtitle_id': self.subtitle_id, 'program_id': self.program_id, 'sub_program_id': self.sub_program_id, 'state_code': self.state_code, 'year': self.year, 'payment': self.payment, 'recipient_count': self.recipient_count, 'base_acres': self.base_acres}
