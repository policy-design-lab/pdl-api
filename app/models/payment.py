from app.models.db import db


class Payment(db.Model):
    __tablename__ = 'payments'
    __table_args__ = {"schema": "pdl"}

    id = db.Column(db.Integer, primary_key=True)
    title_id = db.Column(db.Integer)
    subtitle_id = db.Column(db.Integer)
    program_id = db.Column(db.Integer)
    sub_program_id = db.Column(db.Integer)
    sub_sub_program_id = db.Column(db.Integer)
    practice_category_id = db.Column(db.Integer)
    state_code = db.Column(db.String())
    year = db.Column(db.Integer)
    payment = db.Column(db.Float)
    recipient_count = db.Column(db.Integer)
    contract_count = db.Column(db.Integer)
    base_acres = db.Column(db.Float)
    farm_count = db.Column(db.Integer)
    practice_code = db.Column(db.String())
    practice_code_variant = db.Column(db.String())
    premium_policy_count = db.Column(db.Integer)
    liability_amount = db.Column(db.Integer)
    premium_amount = db.Column(db.Integer)
    premium_subsidy_amount = db.Column(db.Integer)
    indemnity_amount = db.Column(db.Integer)
    farmer_premium_amount = db.Column(db.Integer)
    loss_ratio = db.Column(db.Float)
    net_farmer_benefit_amount = db.Column(db.Integer)

    def __init__(self, title_id, subtitle_id, program_id, sub_program_id, sub_sub_program_id, state_code, year, payment,
                 recipient_count, contract_count, base_acres, farm_count, practice_code, practice_code_variant,
                 premium_policy_count, liability_amount, premium_amount, premium_subsidy_amount, indemnity_amount,
                 farmer_premium_amount, loss_ratio, net_farmer_benefit_amount):
        self.title_id = title_id
        self.subtitle_id = subtitle_id
        self.program_id = program_id
        self.sub_program_id = sub_program_id
        self.sub_sub_program_id = sub_sub_program_id
        self.state_code = state_code
        self.year = year
        self.payment = payment
        self.recipient_count = recipient_count
        self.contract_count = contract_count
        self.base_acres = base_acres
        self.farm_count = farm_count
        self.practice_code = practice_code
        self.practice_code_variant = practice_code_variant
        self.premium_policy_count = premium_policy_count
        self.liability_amount = liability_amount
        self.premium_amount = premium_amount
        self.premium_subsidy_amount = premium_subsidy_amount
        self.indemnity_amount = indemnity_amount
        self.farmer_premium_amount = farmer_premium_amount
        self.loss_ratio = loss_ratio
        self.net_farmer_benefit_amount = net_farmer_benefit_amount

    def __repr__(self):
        return 'Payments(title_id=%s, subtitle_id=%s, program_id=%s, sub_program_id=%s, sub_sub_program_id=%s, ' \
               'state_code=%s, year=%s, payment=%s, recipient_count=%s, contract_count=%s base_acres=%s, ' \
               'farm_count=%s, practice_code=%s, practice_code_variant=%s, premium_policy_count=%s, ' \
               'liability_amount=%s, premium_amount =%s, premium_subsidy_amount=%s, indemnity_amount=%s, ' \
               'farmer_premium_amount=%s, loss_ratio=%s, net_farmer_benefit_amount=%s)' % (
            self.title_id, self.subtitle_id, self.program_id, self.sub_program_id, self.sub_sub_program_id,
            self.state_code, self.year, self.payment, self.recipient_count, self.contract_count, self.base_acres,
            self.farm_count, self.practice_code, self.practice_code_variant, self.premium_policy_count,
            self.liability_amount, self.premium_amount, self.premium_subsidy_amount, self.indemnity_amount,
            self.farmer_premium_amount, self.loss_ratio, self.net_farmer_benefit_amount)

    def json(self):
        return {'title_id': self.title_id, 'subtitle_id': self.subtitle_id, 'program_id': self.program_id,
                'sub_program_id': self.sub_program_id, 'sub_sub_program_id': self.sub_sub_program_id,
                'state_code': self.state_code, 'year': self.year, 'payment': self.payment,
                'recipient_count': self.recipient_count, 'contract_count': self.contract_count,
                'base_acres': self.base_acres, 'farm_count': self.farm_count, 'practice_code': self.practice_code,
                'practice_code_variant': self.practice_code_variant, 'premium_policy_count': self.premium_policy_count,
                'liability_amount': self.liability_amount, 'premium_amount': self.premium_amount,
                'premium_subsidy_amount': self.premium_subsidy_amount, 'indemnity_amount': self.indemnity_amount,
                'farmer_premium_amount': self.farmer_premium_amount, 'loss_ratio': self.loss_ratio,
                'net_farmer_benefit_amount': self.net_farmer_benefit_amount}
