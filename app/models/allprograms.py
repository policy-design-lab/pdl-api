from app.models.db import db


class AllProgram(db.Model):
    __tablename__ = 'allprograms'

    all_program_code = db.Column(db.Integer(), primary_key=True)
    state = db.Column(db.String())
    crop_ins_2018 = db.Column(db.Float())
    crop_ins_2019 = db.Column(db.Float())
    crop_ins_2020 = db.Column(db.Float())
    crop_ins_2021 = db.Column(db.Float())
    crop_ins_2022 = db.Column(db.Float())
    crop_ins_total = db.Column(db.Float())
    snap_2018 = db.Column(db.Float())
    snap_2019 = db.Column(db.Float())
    snap_2020 = db.Column(db.Float())
    snap_2021 = db.Column(db.Float())
    snap_2022 = db.Column(db.Float())
    snap_total = db.Column(db.Float())
    title_1_2018 = db.Column(db.Float())
    title_1_2019 = db.Column(db.Float())
    title_1_2020 = db.Column(db.Float())
    title_1_2021 = db.Column(db.Float())
    title_1_2022 = db.Column(db.Float())
    title_1_total = db.Column(db.Float())
    title_2_2018 = db.Column(db.Float())
    title_2_2019 = db.Column(db.Float())
    title_2_2020 = db.Column(db.Float())
    title_2_2021 = db.Column(db.Float())
    title_2_2022 = db.Column(db.Float())
    title_2_total = db.Column(db.Float())
    all_programs_total_2018 = db.Column(db.Float())
    all_programs_total_2019 = db.Column(db.Float())
    all_programs_total_2020 = db.Column(db.Float())
    all_programs_total_2021 = db.Column(db.Float())
    all_programs_total_2022 = db.Column(db.Float())
    all_programs_total_18_22 = db.Column(db.Float())

    def __init__(self, all_program_code, state, crop_ins_2018, crop_ins_2019, crop_ins_2020, crop_ins_2021,
                 crop_ins_2022, crop_ins_total, snap_2018, snap_2019, snap_2020, snap_2021, snap_2022, snap_total,
                 title_1_2018, title_1_2019, title_1_2020, title_1_2021, title_1_2022, title_1_total,
                 title_2_2018, title_2_2019, title_2_2020, title_2_2021, title_2_2022, title_2_total,
                 all_programs_total_2018, all_programs_total_2019, all_programs_total_2020, all_programs_total_2021,
                 all_programs_total_2022, all_programs_total_18_22):
        self.all_program_code = all_program_code
        self.state = state
        self.crop_ins_2018 = crop_ins_2018
        self.crop_ins_2019 = crop_ins_2019
        self.crop_ins_2020 = crop_ins_2020
        self.crop_ins_2021 = crop_ins_2021
        self.crop_ins_2022 = crop_ins_2022
        self.crop_ins_total = crop_ins_total
        self.snap_2018 = snap_2018
        self.snap_2019 = snap_2019
        self.snap_2020 = snap_2020
        self.snap_2021 = snap_2021
        self.snap_2022 = snap_2022
        self.snap_total = snap_total
        self.title_1_2018 = title_1_2018
        self.title_1_2019 = title_1_2019
        self.title_1_2020 = title_1_2020
        self.title_1_2021 = title_1_2021
        self.title_1_2022 = title_1_2022
        self.title_1_total = title_1_total
        self.title_2_2018 = title_2_2018
        self.title_2_2019 = title_2_2019
        self.title_2_2020 = title_2_2020
        self.title_2_2021 = title_2_2021
        self.title_2_2022 = title_2_2022
        self.title_2_total = title_2_total
        self.all_programs_total_2018 = all_programs_total_2018
        self.all_programs_total_2019 = all_programs_total_2019
        self.all_programs_total_2020 = all_programs_total_2020
        self.all_programs_total_2021 = all_programs_total_2021
        self.all_programs_total_2022 = all_programs_total_2022
        self.all_programs_total_18_22 = all_programs_total_18_22

    def __repr__(self):
        return 'Summary(state=%s, ' \
               'crop_ins_2018=%d, crop_ins_2019=%s, crop_ins_2020=%d, crop_ins_2021=%s, crop_ins_2022=%d, ' \
               'crop_ins_total=%s,snap_2018=%d, snap_2019=%s, snap_2020=%d, snap_2021=%s, snap_2022=%d, ' \
               'snap_total=%s, title_1_2018=%d, title_1_2019=%s, title_1_2020=%d, title_1_2021=%s, title_1_2022=%d, ' \
               'title_1_total=%s, title_2_2018=%d, title_2_2019=%s, title_2_2020=%d, title_2_2021=%s, ' \
               'title_2_2022=%d, title_2_total=%s,all_programs_total_2018=%d, all_programs_total_2019=%s, ' \
               'all_programs_total_2020=%d, all_programs_total_2021=%s, all_programs_total_2022=%d, ' \
               'all_programs_total_18_22=%s)' \
               % (self.state,
                  self.crop_ins_2018, self.crop_ins_2019, self.crop_ins_2020, self.crop_ins_2021, self.crop_ins_2022,
                  self.crop_ins_total, self.snap_2018, self.snap_2019, self.snap_2020, self.snap_2021, self.snap_2022,
                  self.snap_total, self.title_1_2018, self.title_1_2019, self.title_1_2020, self.title_1_2021,
                  self.title_1_2022, self.title_1_total, self.title_2_2018, self.title_2_2019, self.title_2_2020,
                  self.title_2_2021, self.title_2_2022, self.title_2_total, self.all_programs_total_2018,
                  self.all_programs_total_2019, self.all_programs_total_2020, self.all_programs_total_2021,
                  self.all_programs_total_2022, self.all_programs_total_18_22)

    def json(self):
        return {'State': self.state,
                'Crop Insurance 2018': self.crop_ins_2018, 'Crop Insurance 2019': self.crop_ins_2019,
                'Crop Insurance 2020': self.crop_ins_2020, 'Crop Insurance 2021': self.crop_ins_2021,
                'Crop Insurance 2022': self.crop_ins_2022, 'Crop Insurance Total': self.crop_ins_total,
                'SNAP 2018': self.snap_2018, 'SNAP 2019': self.snap_2019,
                'SNAP 2020': self.snap_2020, 'SNAP 2021': self.snap_2021,
                'SNAP 2022': self.snap_2022, 'SNAP Total': self.snap_total,
                'Title I 2018': self.title_1_2018, 'Title I 2019': self.title_1_2019,
                'Title I 2020': self.title_1_2020, 'Title I 2021': self.title_1_2021,
                'Title I 2022': self.title_1_202, 'Title I Total': self.title_1_total,
                'Title II 2018': self.title_2_2018, 'Title II 2019': self.title_2_2019,
                'Title II 2020': self.title_2_2020, 'Title II 2021': self.title_2_2021,
                'Title II 2022': self.title_2_202, 'Title II Total': self.title_2_total,
                '2018 All Programs Total': self.all_programs_total_2018,
                '2019 All Programs Total': self.all_programs_total_2019,
                '2020 All Programs Total': self.all_programs_total_2020,
                '2021 All Programs Total': self.all_programs_total_2021,
                '2022 All Programs Total': self.all_programs_total_2022,
                '18-22 All Programs Total': self.all_programs_total_18_22
                }
