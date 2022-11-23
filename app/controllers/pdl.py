import app.utils.jsonutils as jsonutils

from app.models.summary import Summary
from app.models.state import State
from app.models.allprograms import AllProgram


def search():
    out_json = jsonutils.create_test_message()

    return out_json


# GET all the entries from summary table
def summary_search():
    summaries = Summary.query.all()
    results = [
        {
            "title": summary.title,
            "state": summary.state,
            "fiscal year": summary.fiscal_year,
            "amount": summary.amount
        } for summary in summaries]

    # return {"count": len(results), "summary": results}
    return results


# GET all the entries from states table
def states_search():
    states = State.query.all()
    results = [
        {
            "val": state.state_code,
            "id": state.state_name
        } for state in states]

    # return {"count": len(results), "states": results}
    return results


# GET all the entries from states table
def allprograms_search():
    allprograms = AllProgram.query.all()
    results = [
        {
            'State': prog.state,
            'Crop Insurance 2018': prog.crop_ins_2018,
            'Crop Insurance 2019': prog.crop_ins_2019,
            'Crop Insurance 2020': prog.crop_ins_2020,
            'Crop Insurance 2021': prog.crop_ins_2021,
            'Crop Insurance 2022': prog.crop_ins_2022,
            'Crop Insurance Total': prog.crop_ins_total,
            'SNAP 2018': prog.snap_2018,
            'SNAP 2019': prog.snap_2019,
            'SNAP 2020': prog.snap_2020,
            'SNAP 2021': prog.snap_2021,
            'SNAP 2022': prog.snap_2022,
            'SNAP Total': prog.snap_total,
            'Title I 2018': prog.title_1_2018,
            'Title I 2019': prog.title_1_2019,
            'Title I 2020': prog.title_1_2020,
            'Title I 2021': prog.title_1_2021,
            'Title I 2022': prog.title_1_2022,
            'Title I Total': prog.title_1_total,
            'Title II 2018': prog.title_2_2018,
            'Title II 2019': prog.title_2_2019,
            'Title II 2020': prog.title_2_2020,
            'Title II 2021': prog.title_2_2021,
            'Title II 2022': prog.title_2_2022,
            'Title II Total': prog.title_2_total,
            '2018 All Programs Total': prog.all_programs_total_2018,
            '2019 All Programs Total': prog.all_programs_total_2019,
            '2020 All Programs Total': prog.all_programs_total_2020,
            '2021 All Programs Total': prog.all_programs_total_2021,
            '2022 All Programs Total': prog.all_programs_total_2022,
            '18-22 All Programs Total': prog.all_programs_total_18_22
        } for prog in allprograms]

    # return {"count": len(results), "states": results}
    return results