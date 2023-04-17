import logging
import json
import os
import app.utils.jsonutils as jsonutils
import app.utils.rest_handlers as rs_handlers

from flask import request
from app.models.summary import Summary
from app.models.state import State
from app.models.statecode import StateCode
from app.models.allprograms import AllProgram

COMMOD_JSON_DATA_PATH = os.path.join("controllers", "data", "commodities")
COMMOD_MAP_DATA_JSON = "commodities_map_data.json"
COMMOD_STATE_DISTRIBUTION_DATA_JSON = "commodities_state_distribution_data.json"
COMMOD_SUBPROGRAMS_DATA_JSON = "commodities_subprograms_data.json"
CSP_JSON_DATA_PATH = os.path.join("controllers", "data", "conservation", "csp")
CSP_MAP_DATA_JSON = "csp_map_data.json"
CSP_STATE_DISTRIBUTION_DATA_JSON = "csp_state_distribution_data.json"
CSP_PRACTICE_CATEGORIES_DATA_JSON = "csp_practice_categories_data.json"
EQIP_JSON_DATA_PATH = os.path.join("controllers", "data", "conservation", "eqip")
SNAP_JSON_DATA_PATH = os.path.join("controllers", "data", "snap")
SNAP_DATA_JSON = "snap_state_distribution_data.json"
EQIP_JSON_DATA_PATH = os.path.join("controllers", "data", "conservation", "eqip")
EQIP_MAP_DATA_JSON = "eqip_map_data.json"
EQIP_STATE_DISTRIBUTION_DATA_JSON = "eqip_state_distribution_data.json"
EQIP_PRACTICE_CATEGORIES_DATA_JSON = "eqip_practice_categories_data.json"


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
        summaries = Summary.query.filter_by(state=state.upper()).all()
        results = [construct_summary_result(summary) for summary in summaries]

        return results

    # only year provide
    elif not state and year is not None:
        summaries = Summary.query.filter_by(fiscal_year=year).all()
        results = [construct_summary_result(summary) for summary in summaries]

        return results

    # both year and name provided
    elif state and year:
        summaries = Summary.query.filter((Summary.fiscal_year == year) & (Summary.state == state.upper())).all()
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
def states_search(code=None, fips=None):
    # there is no code or no fips
    if not code and not fips:
        states = State.query.all()
        results = [construct_state_result(state) for state in states]
        return results

    # yes code and no fips
    elif code is not None and not fips:
        states = State.query.filter_by(state_code=code.upper()).all()
        results = [construct_state_result(state) for state in states]
        return results

    # no code and yes fips
    elif not code and fips is not None:
        states = State.query.filter_by(state_fips=fips).all()
        results = [construct_state_result(state) for state in states]
        return results

    # yes code and yes fips
    elif code is not None and fips is not None:
        states = State.query.filter((State.state_fips == fips) & (State.state_code == code.upper())).all()
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


# GET states by state code
def states_get(statecode=None):
    if not statecode:
        msg = {
            "reason": "Must provide name abbreviation",
            "error": "Bad Request: " + request.url,
        }
        logging.error("State " + json.dumps(msg))
        return rs_handlers.bad_request(msg)
    else:
        state = State.query.filter_by(state_code=statecode.upper()).first()
        if state is None:
            msg = {
                "reason": "No record for the given state code " + statecode,
                "error": "Not found: " + request.url,
            }
            logging.error("State" + json.dumps(msg))
            return rs_handlers.not_found(msg)
        else:
            result = construct_state_result(state)
            return result


# GET all the entries from statecodes table
def statecodes_search(code=None, name=None):
    # there is no code or no name
    if not code and not name:
        states = StateCode.query.all()
        results = [construct_statecode_result(state) for state in states]
        return results

    # yes code and no name
    elif code is not None and not name:
        states = StateCode.query.filter_by(state_code=code.upper()).all()
        results = [construct_statecode_result(state) for state in states]
        return results

    # no code and yes name
    elif not code and name is not None:
        states = StateCode.query.filter_by(state_name=name).all()
        results = [construct_statecode_result(state) for state in states]
        return results

    # yes code and yes name
    elif code is not None and name is not None:
        states = StateCode.query.filter((StateCode.state_name == name) & (StateCode.state_code == code.upper())).all()
        results = [construct_statecode_result(state) for state in states]
        return results

    # none of them
    else:
        msg = {
            "reason": "The query is not correct.",
            "error": "Bad Request: " + request.url,
        }
        logging.error("States " + json.dumps(msg))
        return rs_handlers.bad_request(msg)


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


# SNAP state distribution data
def programs_snap_state_distribution_search():
    # set the file path
    eqip_data = os.path.join(SNAP_JSON_DATA_PATH, SNAP_DATA_JSON)

    # open file
    with open(eqip_data, 'r') as map_data:
        file_data = map_data.read()

    # parse file
    data_json = json.loads(file_data)

    return data_json


# commodities map data
def programs_commodities_map_search():
    # set the file path
    csp_data = os.path.join(COMMOD_JSON_DATA_PATH, COMMOD_MAP_DATA_JSON)

    # open file
    with open(csp_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data)

        return data_json


# Commodities state distribution data
def programs_commodities_state_distribution_search():
    # set the file path
    csp_data = os.path.join(COMMOD_JSON_DATA_PATH, COMMOD_STATE_DISTRIBUTION_DATA_JSON)

    # open file
    with open(csp_data, 'r') as state_data:
        file_data = state_data.read()

    # parse file
    data_json = json.loads(file_data)

    return data_json


# Commodities subprogram data
def programs_commodities_subprograms_search():
    # set the file path
    csp_data = os.path.join(COMMOD_JSON_DATA_PATH, COMMOD_SUBPROGRAMS_DATA_JSON)

    # open file
    with open(csp_data, 'r') as subprograms_data:
        file_data = subprograms_data.read()

    # parse file
    data_json = json.loads(file_data)

    return data_json


# CSP map data
def programs_conservation_csp_map_search():
    # set the file path
    csp_data = os.path.join(CSP_JSON_DATA_PATH, CSP_MAP_DATA_JSON)

    # open file
    with open(csp_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data)

        return data_json


# CSP state distribution data
def programs_conservation_csp_state_distribution_search():
    # set the file path
    csp_data = os.path.join(CSP_JSON_DATA_PATH, CSP_STATE_DISTRIBUTION_DATA_JSON)

    # open file
    with open(csp_data, 'r') as state_data:
        file_data = state_data.read()

    # parse file
    data_json = json.loads(file_data)

    return data_json


# CSP practice category data
def programs_conservation_csp_practice_categories_search():
    # set the file path
    csp_data = os.path.join(CSP_JSON_DATA_PATH, CSP_PRACTICE_CATEGORIES_DATA_JSON)

    # open file
    with open(csp_data, 'r') as practice_data:
        file_data = practice_data.read()

    # parse file
    data_json = json.loads(file_data)

    return data_json


# EQIP Map Data
def programs_conservation_eqip_map_search():
    # set the file path
    eqip_data = os.path.join(EQIP_JSON_DATA_PATH, EQIP_MAP_DATA_JSON)

    # open file
    with open(eqip_data, 'r') as map_data:
        file_data = map_data.read()

    # parse file
    data_json = json.loads(file_data)

    return data_json


# EQIP payment distribution data for all states
def programs_conservation_eqip_state_distribution_search():
    # set the file path
    eqip_data = os.path.join(EQIP_JSON_DATA_PATH, EQIP_STATE_DISTRIBUTION_DATA_JSON)

    # open file
    with open(eqip_data, 'r') as map_data:
        file_data = map_data.read()

    # parse file
    data_json = json.loads(file_data)

    return data_json


# EQIP payment distribution data by practice categories
def programs_conservation_eqip_practice_categories_search():
    # set the file path
    eqip_data = os.path.join(EQIP_JSON_DATA_PATH, EQIP_PRACTICE_CATEGORIES_DATA_JSON)

    # open file
    with open(eqip_data, 'r') as map_data:
        file_data = map_data.read()

    # parse file
    data_json = json.loads(file_data)

    return data_json


# construct state
def construct_state_result(state):
    result = {
        "val": state.state_fips,
        "id": state.state_code
    }

    return result


# construct statecode
def construct_statecode_result(state):
    result = {
        "code": state.state_code,
        "name": state.state_name
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
