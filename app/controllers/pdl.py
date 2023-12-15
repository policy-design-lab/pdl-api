import logging
import json
import os
import app.utils.jsonutils as jsonutils
import app.utils.rest_handlers as rs_handlers

from flask import request
from app.models.state import State
from app.models.statecode import StateCode
from collections import OrderedDict

LANDING_PAGE_DATA_PATH = os.path.join("controllers", "data", "landingpage")
ALLPROGRAM_DATA_JSON = "allprograms.json"
SUMMARY_DATA_JSON = "summary.json"
COMMOD_JSON_DATA_PATH = os.path.join("controllers", "data", "commodities")
COMMOD_MAP_DATA_JSON = "commodities_map_data.json"
COMMOD_STATE_DISTRIBUTION_DATA_JSON = "commodities_state_distribution_data.json"
COMMOD_SUBPROGRAMS_DATA_JSON = "commodities_subprograms_data.json"
DMC_STATE_DISTRIBUTION_DATA_JSON = "dmc_state_distribution_data.json"
DMC_SUBPROGRAMS_DATA_JSON = "dmc_subprograms_data.json"
SADA_STATE_DISTRIBUTION_DATA_JSON = "sada_state_distribution_data.json"
SADA_SUBPROGRAMS_DATA_JSON = "sada_subprograms_data.json"
CSP_JSON_DATA_PATH = os.path.join("controllers", "data", "conservation", "csp")
CSP_MAP_DATA_JSON = "csp_map_data.json"
CSP_STATE_DISTRIBUTION_DATA_JSON = "csp_state_distribution_data.json"
CSP_PRACTICE_CATEGORIES_DATA_JSON = "csp_practice_categories_data.json"
CRP_JSON_DATA_PATH = os.path.join("controllers", "data", "conservation", "crp")
CRP_STATE_DISTRIBUTION_DATA_JSON = "crp_state_distribution_data.json"
CRP_SUBPROGRAMS_DATA_JSON = "crp_subprograms_data.json"
ACEP_JSON_DATA_PATH = os.path.join("controllers", "data", "conservation", "acep")
ACEP_STATE_DISTRIBUTION_DATA_JSON = "acep_state_distribution_data.json"
ACEP_SUBPROGRAMS_DATA_JSON = "acep_subprograms_data.json"
RCPP_JSON_DATA_PATH = os.path.join("controllers", "data", "conservation", "rcpp")
RCPP_STATE_DISTRIBUTION_DATA_JSON = "rcpp_state_distribution_data.json"
RCPP_SUBPROGRAMS_DATA_JSON = "rcpp_subprograms_data.json"
SNAP_JSON_DATA_PATH = os.path.join("controllers", "data", "snap")
SNAP_DATA_JSON = "snap_state_distribution_data.json"
EQIP_JSON_DATA_PATH = os.path.join("controllers", "data", "conservation", "eqip")
EQIP_MAP_DATA_JSON = "eqip_map_data.json"
EQIP_STATE_DISTRIBUTION_DATA_JSON = "eqip_state_distribution_data.json"
EQIP_PRACTICE_CATEGORIES_DATA_JSON = "eqip_practice_categories_data.json"
SNAP_JSON_DATA_PATH = os.path.join("controllers", "data", "snap")
SNAP_DATA_JSON = "snap_state_distribution_data.json"
CROP_INSURANCE_JSON_DATA_PATH = os.path.join("controllers", "data", "crop-insurance")
CROP_INSURANCE_SUMMARY_DATA_JSON = "crop_insurance_subprograms_data.json"
CROP_INSURANCE_STATE_DISTRIBUTION_DATA_JSON = "crop_insurance_state_distribution_data.json"


def search():
    out_json = jsonutils.create_test_message()

    return out_json


# GET all the entries from summary table
def summary_search():
    summary_data = os.path.join(LANDING_PAGE_DATA_PATH, SUMMARY_DATA_JSON)

    # open file
    with open(summary_data, 'r') as json_data:
        file_data = json_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


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
def allprograms_search():
    allprograms_data = os.path.join(LANDING_PAGE_DATA_PATH, ALLPROGRAM_DATA_JSON)

    # open file
    with open(allprograms_data, 'r') as json_data:
        file_data = json_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# SNAP state distribution data
def programs_snap_state_distribution_search():
    # set the file path
    eqip_data = os.path.join(SNAP_JSON_DATA_PATH, SNAP_DATA_JSON)

    # open file
    with open(eqip_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# commodities map data
def programs_commodities_map_search():
    # set the file path
    csp_data = os.path.join(COMMOD_JSON_DATA_PATH, COMMOD_MAP_DATA_JSON)

    # open file
    with open(csp_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# Commodities state distribution data
def programs_commodities_state_distribution_search():
    # set the file path
    csp_data = os.path.join(COMMOD_JSON_DATA_PATH, COMMOD_STATE_DISTRIBUTION_DATA_JSON)

    # open file
    with open(csp_data, 'r') as state_data:
        file_data = state_data.read()

    # parse file
    data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

    return data_json


# Commodities subprogram data
def programs_commodities_subprograms_search():
    # set the file path
    csp_data = os.path.join(COMMOD_JSON_DATA_PATH, COMMOD_SUBPROGRAMS_DATA_JSON)

    # open file
    with open(csp_data, 'r') as subprograms_data:
        file_data = subprograms_data.read()

    # parse file
    data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

    return data_json


# DMC state distribution data
def programs_commodities_dmc_state_distribution_search():
    # set the file path
    dmc_data = os.path.join(COMMOD_JSON_DATA_PATH, DMC_STATE_DISTRIBUTION_DATA_JSON)

    # open file
    with open(dmc_data, 'r') as state_data:
        file_data = state_data.read()

    # parse file
    data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

    return data_json


# DMC practice subprograms data
def programs_commodities_dmc_subprograms_search():
    # set the file path
    dmc_data = os.path.join(COMMOD_JSON_DATA_PATH, DMC_SUBPROGRAMS_DATA_JSON)

    # open file
    with open(dmc_data, 'r') as practice_data:
        file_data = practice_data.read()

    # parse file
    data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

    return data_json


# SADA state distribution data
def programs_commodities_sada_state_distribution_search():
    # set the file path
    dmc_data = os.path.join(COMMOD_JSON_DATA_PATH, SADA_STATE_DISTRIBUTION_DATA_JSON)

    # open file
    with open(dmc_data, 'r') as state_data:
        file_data = state_data.read()

    # parse file
    data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

    return data_json


# SADA practice subprograms data
def programs_commodities_sada_subprograms_search():
    # set the file path
    dmc_data = os.path.join(COMMOD_JSON_DATA_PATH, SADA_SUBPROGRAMS_DATA_JSON)

    # open file
    with open(dmc_data, 'r') as practice_data:
        file_data = practice_data.read()

    # parse file
    data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

    return data_json


# CSP map data
def programs_conservation_csp_map_search():
    # set the file path
    csp_data = os.path.join(CSP_JSON_DATA_PATH, CSP_MAP_DATA_JSON)

    # open file
    with open(csp_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# CSP state distribution data
def programs_conservation_csp_state_distribution_search():
    # set the file path
    csp_data = os.path.join(CSP_JSON_DATA_PATH, CSP_STATE_DISTRIBUTION_DATA_JSON)

    # open file
    with open(csp_data, 'r') as state_data:
        file_data = state_data.read()

    # parse file
    data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

    return data_json


# CSP practice category data
def programs_conservation_csp_practice_categories_search():
    # set the file path
    csp_data = os.path.join(CSP_JSON_DATA_PATH, CSP_PRACTICE_CATEGORIES_DATA_JSON)

    # open file
    with open(csp_data, 'r') as practice_data:
        file_data = practice_data.read()

    # parse file
    data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

    return data_json


# CRP state distribution data
def programs_conservation_crp_state_distribution_search():
    # set the file path
    crp_data = os.path.join(CRP_JSON_DATA_PATH, CRP_STATE_DISTRIBUTION_DATA_JSON)

    # open file
    with open(crp_data, 'r') as state_data:
        file_data = state_data.read()

    # parse file
    data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

    return data_json


# CRP practice category data
def programs_conservation_crp_subprograms_search():
    # set the file path
    crp_data = os.path.join(CRP_JSON_DATA_PATH, CRP_SUBPROGRAMS_DATA_JSON)

    # open file
    with open(crp_data, 'r') as practice_data:
        file_data = practice_data.read()

    # parse file
    data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

    return data_json


# ACEP state distribution data
def programs_conservation_acep_state_distribution_search():
    # set the file path
    acep_data = os.path.join(ACEP_JSON_DATA_PATH, ACEP_STATE_DISTRIBUTION_DATA_JSON)

    # open file
    with open(acep_data, 'r') as state_data:
        file_data = state_data.read()

    # parse file
    data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

    return data_json


# ACEP practice subprograms data
def programs_conservation_acep_subprograms_search():
    # set the file path
    acep_data = os.path.join(ACEP_JSON_DATA_PATH, ACEP_SUBPROGRAMS_DATA_JSON)

    # open file
    with open(acep_data, 'r') as practice_data:
        file_data = practice_data.read()

    # parse file
    data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

    return data_json
  

# RCPP state distribution data
def programs_conservation_rcpp_state_distribution_search():
    # set the file path
    rcpp_data = os.path.join(RCPP_JSON_DATA_PATH, RCPP_STATE_DISTRIBUTION_DATA_JSON)

    # open file
    with open(rcpp_data, 'r') as state_data:
        file_data = state_data.read()
      
    # parse file
    data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

    return data_json


# RCPP practice subprograms data
def programs_conservation_rcpp_subprograms_search():
    # set the file path
    rcpp_data = os.path.join(RCPP_JSON_DATA_PATH, RCPP_SUBPROGRAMS_DATA_JSON)

    # open file
    with open(rcpp_data, 'r') as practice_data:
        file_data = practice_data.read()
      
    # parse file
    data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

    return data_json


# EQIP Map Data
def programs_conservation_eqip_map_search():
    # set the file path
    eqip_data = os.path.join(EQIP_JSON_DATA_PATH, EQIP_MAP_DATA_JSON)

    # open file
    with open(eqip_data, 'r') as map_data:
        file_data = map_data.read()

    # parse file
    data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

    return data_json


# EQIP payment distribution data for all states
def programs_conservation_eqip_state_distribution_search():
    # set the file path
    eqip_data = os.path.join(EQIP_JSON_DATA_PATH, EQIP_STATE_DISTRIBUTION_DATA_JSON)

    # open file
    with open(eqip_data, 'r') as map_data:
        file_data = map_data.read()

    # parse file
    data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

    return data_json


# EQIP payment distribution data by practice categories
def programs_conservation_eqip_practice_categories_search():
    # set the file path
    eqip_data = os.path.join(EQIP_JSON_DATA_PATH, EQIP_PRACTICE_CATEGORIES_DATA_JSON)

    # open file
    with open(eqip_data, 'r') as map_data:
        file_data = map_data.read()

    # parse file
    data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

    return data_json


# Crop Insurance payment distribution data for all states
def programs_crop_insurance_state_distribution_search():
    # set the file path
    eqip_data = os.path.join(CROP_INSURANCE_JSON_DATA_PATH, CROP_INSURANCE_STATE_DISTRIBUTION_DATA_JSON)

    # open file
    with open(eqip_data, 'r') as map_data:
        file_data = map_data.read()

    # parse file
    data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

    return data_json


# Crop Insurance summary data for all states
def programs_crop_insurance_summary_search():
    # set the file path
    eqip_data = os.path.join(CROP_INSURANCE_JSON_DATA_PATH, CROP_INSURANCE_SUMMARY_DATA_JSON)

    # open file
    with open(eqip_data, 'r') as map_data:
        file_data = map_data.read()

    # parse file
    data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

    return data_json

# /pdl/titles/title-i/subtitles/subtitle-a/map:
# /pdl/titles/title-i/subtitles/subtitle-a/state-distribution:
# /pdl/titles/title-i/subtitles/subtitle-a/subprograms:
#
# /pdl/titles/title-i/subtitles/subtitle-d/state-distribution:
# /pdl/titles/title-i/subtitles/subtitle-d/subprograms:
#
# /pdl/titles/title-i/subtitles/subtitle-e/state-distribution:
# /pdl/titles/title-i/subtitles/subtitle-e/subprograms:
#
# /pdl/titles/title-ii/programs/eqip/map
# /pdl/titles/title-ii/programs/eqip/state-distribution
# /pdl/titles/title-ii/programs/eqip/practice-categories
#
# /pdl/titles/title-ii/programs/csp/map
# /pdl/titles/title-ii/programs/csp/state-distribution
# /pdl/titles/title-ii/programs/csp/practice-categories
#
# /pdl/titles/title-ii/programs/crp/state-distribution
# /pdl/titles/title-ii/programs/crp/subprograms
#
# /pdl/titles/title-ii/programs/acep/state-distribution
# /pdl/titles/title-ii/programs/acep/subprograms
#
# /pdl/titles/title-ii/programs/rcpp/state-distribution
# /pdl/titles/title-ii/programs/rcpp/subprograms


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
        "Title": summary.title,
        "State": summary.state,
        "Fiscal Year": summary.fiscal_year,
        "Amount": summary.amount
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
