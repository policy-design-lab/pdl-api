import logging
import json
import app.utils.jsonutils as jsonutils
import app.utils.rest_handlers as rs_handlers

from flask import request
from app.models.summary import Summary
from app.models.state import State
from app.models.allprograms import AllProgram


def search():
    out_json = jsonutils.create_test_message()

    return out_json


# GET all the entries from summary table
def summary_search(state=None, year=None):
    if not state and not year:
        summaries = Summary.query.all()
        results = [construct_summary_result(summary) for summary in summaries]

        # return {"count": len(results), "summary": results}
        return results

    # only name provide
    elif state is not None and not year:
        summaries = Summary.query.filter_by(state = state.upper()).all()
        results = [construct_summary_result(summary) for summary in summaries]

        return results

    # only year provide
    elif not state and year is not None:
        summaries = Summary.query.filter_by(fiscal_year = year).all()
        results = [construct_summary_result(summary) for summary in summaries]

        return results

    # both year and name provided
    elif state and year:
        summaries = Summary.query.filter((Summary.fiscal_year==year) & (Summary.state==state.upper())).all()
        results = [construct_summary_result(summary) for summary in summaries]

        return results

    # none of them
    else:
        msg = {
            "reason": "The query is not correct.",
            "error": "Bad Request: " + request.url,
        }
        logging.error("Summary " + json.dumps(msg))
        return rs_handlers.bad_request(msg)


# GET all the entries from states table
def states_search(name=None, fips=None):
    # there is no name or no fips
    if not name and not fips:
        states = State.query.all()
        results = [construct_state_result(state) for state in states]
        return results

    # yes name and no fips
    elif name is not None and not fips:
        states = State.query.filter_by(state_name = name.upper()).all()
        results = [construct_state_result(state) for state in states]
        return results

    # no name and yes fips
    elif not name and fips is not None:
        states = State.query.filter_by(state_code=fips).all()
        results = [construct_state_result(state) for state in states]
        return results

    # yes name and yes fips
    elif name is not None and fips is not None:
        states = State.query.filter((State.state_code==fips) & (State.state_name == name.upper())).all()
        results = [construct_state_result(state) for state in states]
        return results

    # none of them
    else:
        msg = {
            "reason": "The query is not correct.",
            "error": "Bad Request: " + request.url,
        }
        logging.error("States " + json.dumps(msg))
        return rs_handlers.bad_request(msg)


# GET states by statename
def states_get(statename=None):
    if not statename:
        msg = {
            "reason": "Must provide name abbreviation",
            "error": "Bad Request: " + request.url,
        }
        logging.error("State " + json.dumps(msg))
        return rs_handlers.bad_request(msg)
    else:
        state = State.query.filter_by(state_name = statename.upper()).first()
        if state is None:
            msg = {
                "reason": "No record for the given name abbreviation " + statename,
                "error": "Not found: " + request.url,
            }
            logging.error("State" + json.dumps(msg))
            return rs_handlers.not_found(msg)
        else:
            result = construct_state_result(state)
            return result


# GET all the entries from states table
def allprograms_search(state=None):
    # no state parameters
    if not state:
        allprograms = AllProgram.query.all()
        results = [construct_allprogram_result(prog) for prog in allprograms]
        return results

    # yes state
    elif state is not None:
        allprograms = AllProgram.query.filter_by(state=state.upper()).all()
        results = [construct_allprogram_result(prog) for prog in allprograms]
        return results

    # none of them
    else:
        msg = {
            "reason": "The query is not correct.",
            "error": "Bad Request: " + request.url,
        }
        logging.error("All programs " + json.dumps(msg))
        return rs_handlers.bad_request(msg)


# construct name
def construct_state_result(state):
    result = {
        "val": state.state_code,
        "id": state.state_name
    }

    return result


# construct summary
def construct_summary_result(summary):
    result = {
        "title": summary.title,
        "state": summary.state,
        "fiscal year": summary.fiscal_year,
        "amount": summary.amount
    }

    return result


# construct all programs
def construct_allprogram_result(prog):
    result = {
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
    }

    return result
