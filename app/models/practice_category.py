from app.models.db import db


class PracticeCategory(db.Model):
    __tablename__ = 'practice_categories'
    __table_args__ = {"schema": "pdl"}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    display_name = db.Column(db.String())
    category_grouping = db.Column(db.String())
    program_id = db.Column(db.Integer)
    is_statutory_category = db.Column(db.Boolean)

    def __init__(self, name, display_name, category_grouping, program_id, is_statutory_category):
        self.name = name
        self.display_name = display_name
        self.category_grouping = category_grouping
        self.program_id = program_id
        self.is_statutory_category = is_statutory_category

    def __repr__(self):
        return 'ProgramCategories(name=%s, display_name=%s, category_grouping=%s, program_id=%s, is_statutory_category=%s)' % (
            self.name, self.display_name, self.category_grouping, self.program_id, self.is_statutory_category)

    def json(self):
        return {'name': self.name, 'display_name': self.display_name, 'category_grouping': self.category_grouping, 'program_id': self.program_id, 'is_statutory_category': self.is_statutory_category}
