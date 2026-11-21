from app.models.db import db


class PaymentByStateFromCounties(db.Model):
    __tablename__ = 'payments_by_state_from_counties'
    __table_args__ = {"schema": "pdl"}

    title_id = db.Column(db.SmallInteger, primary_key=True)
    program_id = db.Column(db.SmallInteger, primary_key=True)
    year = db.Column(db.SmallInteger, primary_key=True)
    state_code = db.Column(db.String(), primary_key=True)

    subtitle_id = db.Column(db.Integer)
    sub_program_id = db.Column(db.Integer)
    sub_sub_program_id = db.Column(db.Integer)
    practice_category_id = db.Column(db.Integer)
    payment = db.Column(db.Numeric)
    recipient_count = db.Column(db.BigInteger)
    base_acres = db.Column(db.Numeric)
    farm_count = db.Column(db.BigInteger)
    contract_count = db.Column(db.BigInteger)
    practice_code = db.Column(db.Text)
    practice_code_variant = db.Column(db.Text)
    premium_policy_count = db.Column(db.Numeric)
    liability_amount = db.Column(db.Numeric)
    premium_amount = db.Column(db.Numeric)
    premium_subsidy_amount = db.Column(db.Numeric)
    indemnity_amount = db.Column(db.Numeric)
    farmer_premium_amount = db.Column(db.Numeric)
    loss_ratio = db.Column(db.Numeric)
    net_farmer_benefit_amount = db.Column(db.Numeric)
