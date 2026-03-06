
from app.models.db import db


class PaymentByCounty(db.Model):
    __tablename__ = 'payments_by_counties'
    __table_args__ = {"schema": "pdl"}

    id = db.Column(db.Integer, primary_key=True)
    title_id = db.Column(db.Integer)
    subtitle_id = db.Column(db.Integer)
    program_id = db.Column(db.Integer)
    sub_program_id = db.Column(db.Integer)
    sub_sub_program_id = db.Column(db.Integer)
    practice_category_id = db.Column(db.Integer)
    county_fips_code = db.Column(db.String())
    year = db.Column(db.Integer)
    payment = db.Column(db.Float)
    recipient_count = db.Column(db.Integer)
    base_acres = db.Column(db.Float)
    farm_count = db.Column(db.Integer)
    contract_count = db.Column(db.Integer)
    premium_policy_count = db.Column(db.Integer)
    liability_amount = db.Column(db.BigInteger)
    premium_amount = db.Column(db.BigInteger)
    premium_subsidy_amount = db.Column(db.BigInteger)
    indemnity_amount = db.Column(db.BigInteger)
    farmer_premium_amount = db.Column(db.BigInteger)
    loss_ratio = db.Column(db.Float)
    net_farmer_benefit_amount = db.Column(db.BigInteger)
    practice_code = db.Column(db.String())
    practice_code_variant = db.Column(db.String())

    def __init__(self, title_id, subtitle_id, program_id, sub_program_id, sub_sub_program_id,
                 practice_category_id, county_fips_code, year, payment, recipient_count, base_acres,
                 farm_count, contract_count, premium_policy_count, liability_amount, premium_amount,
                 premium_subsidy_amount, indemnity_amount, farmer_premium_amount, loss_ratio,
                 net_farmer_benefit_amount, practice_code, practice_code_variant):
        self.title_id = title_id
        self.subtitle_id = subtitle_id
        self.program_id = program_id
        self.sub_program_id = sub_program_id
        self.sub_sub_program_id = sub_sub_program_id
        self.practice_category_id = practice_category_id
        self.county_fips_code = county_fips_code
        self.year = year
        self.payment = payment
        self.recipient_count = recipient_count
        self.base_acres = base_acres
        self.farm_count = farm_count
        self.contract_count = contract_count
        self.premium_policy_count = premium_policy_count
        self.liability_amount = liability_amount
        self.premium_amount = premium_amount
        self.premium_subsidy_amount = premium_subsidy_amount
        self.indemnity_amount = indemnity_amount
        self.farmer_premium_amount = farmer_premium_amount
        self.loss_ratio = loss_ratio
        self.net_farmer_benefit_amount = net_farmer_benefit_amount
        self.practice_code = practice_code
        self.practice_code_variant = practice_code_variant

    def json(self):
        return {
            'title_id': self.title_id,
            'subtitle_id': self.subtitle_id,
            'program_id': self.program_id,
            'sub_program_id': self.sub_program_id,
            'sub_sub_program_id': self.sub_sub_program_id,
            'practice_category_id': self.practice_category_id,
            'county_fips_code': self.county_fips_code,
            'year': self.year,
            'payment': self.payment,
            'recipient_count': self.recipient_count,
            'base_acres': self.base_acres,
            'farm_count': self.farm_count,
            'contract_count': self.contract_count,
            'premium_policy_count': self.premium_policy_count,
            'liability_amount': self.liability_amount,
            'premium_amount': self.premium_amount,
            'premium_subsidy_amount': self.premium_subsidy_amount,
            'indemnity_amount': self.indemnity_amount,
            'farmer_premium_amount': self.farmer_premium_amount,
            'loss_ratio': self.loss_ratio,
            'net_farmer_benefit_amount': self.net_farmer_benefit_amount,
            'practice_code': self.practice_code,
            'practice_code_variant': self.practice_code_variant
        }