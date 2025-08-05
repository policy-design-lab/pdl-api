import gzip
import json
import logging
import os
from collections import OrderedDict
from app.controllers.configs import Config as cfg
from flask import request, Response
from sqlalchemy import func, desc, Numeric, BigInteger, Integer, text, or_, and_

import app.utils.jsonutils as jsonutils
import app.utils.rest_handlers as rs_handlers
from app.models.db import Session
from app.models.payment import Payment
from app.models.practice import Practice
from app.models.program import Program
from app.models.practice_category import PracticeCategory
from app.models.state import State
from app.models.statecode import StateCode
from app.models.sub_subprogram import SubSubProgram
from app.models.subprogram import SubProgram
from app.models.subtitle import Subtitle
from app.models.title import Title
from collections import defaultdict

LANDING_PAGE_DATA_PATH = os.path.join("controllers", "data", "landingpage")
ALLPROGRAM_DATA_JSON = "allprograms.json"
SUMMARY_DATA_JSON = "summary.json"

TITLE_I_DATA_PATH = os.path.join("controllers", "data", "title-i")
I_SUBTITLE_A_DATA_PATH = os.path.join(TITLE_I_DATA_PATH, "subtitle-a")
COMMOD_MAP_DATA_JSON = "commodities_map_data.json"
COMMOD_STATE_DISTRIBUTION_DATA_JSON = "commodities_state_distribution_data.json"
COMMOD_SUBPROGRAMS_DATA_JSON = "commodities_subprograms_data.json"
ARC_PLC_DATA_JSON = "arc_plc_payments_current.json.gz"
ARC_PLC_CURRENT_OBBBA_DATA_JSON = "arc_plc_payments_current_obbba.json.gz"
ARC_PLC_PROPOSED_OBBBA_DATA_JSON = "arc_plc_payments_proposed_obbba.json.gz"
I_PROPOSALS_SUBTITLE_A_DATA_PATH = os.path.join(TITLE_I_DATA_PATH, "proposals", "subtitle-a")
ARC_PLC_PROPOSAL_DATA_JSON = "arc_plc_payments_proposed.json.gz"
I_SUBTITLE_D_DATA_PATH = os.path.join(TITLE_I_DATA_PATH, "subtitle-d")
DMC_STATE_DISTRIBUTION_DATA_JSON = "dmc_state_distribution_data.json"
DMC_SUBPROGRAMS_DATA_JSON = "dmc_subprograms_data.json"
I_SUBTITLE_E_DATA_PATH = os.path.join(TITLE_I_DATA_PATH, "subtitle-e")
SADA_STATE_DISTRIBUTION_DATA_JSON = "sada_state_distribution_data.json"
SADA_SUBPROGRAMS_DATA_JSON = "sada_subprograms_data.json"

TITLE_II_DATA_PATH = os.path.join("controllers", "data", "title-ii")
II_EQIP_DATA_PATH = os.path.join(TITLE_II_DATA_PATH, "programs", "eqip")
II_EQIP_IRA_DATA_PATH = os.path.join(TITLE_II_DATA_PATH, "programs", "eqip-ira")
EQIP_MAP_DATA_JSON = "eqip_map_data.json"
EQIP_STATE_DISTRIBUTION_DATA_JSON = "eqip_state_distribution_data.json"
EQIP_PRACTICE_CATEGORIES_DATA_JSON = "eqip_practice_categories_data.json"
EQIP_IRA_STATE_DISTRIBUTION_DATA_JSON = "eqip_ira_state_distribution.json"
EQIP_IRA_SUMMARY_DATA_JSON = "eqip_ira_summary.json"
EQIP_IRA_PRACTICE_CATEGORIES_DATA_JSON = "eqip_ira_practices.json"
EQIP_IRA_AGGREGATE_DATA_JSON = "eqip_ira_aggregated_prediction.json"
II_CSP_DATA_PATH = os.path.join(TITLE_II_DATA_PATH, "programs", "csp")
CSP_MAP_DATA_JSON = "csp_map_data.json"
CSP_STATE_DISTRIBUTION_DATA_JSON = "csp_state_distribution_data.json"
CSP_PRACTICE_CATEGORIES_DATA_JSON = "csp_practice_categories_data.json"
II_CSP_IRA_DATA_PATH = os.path.join(TITLE_II_DATA_PATH, "programs", "csp-ira")
CSP_IRA_STATE_DISTRIBUTION_DATA_JSON = "csp_ira_state_distribution.json"
CSP_IRA_SUMMARY_DATA_JSON = "csp_ira_summary.json"
CSP_IRA_PRACTICE_CATEGORIES_DATA_JSON = "csp_ira_practices.json"
CSP_IRA_AGGREGATE_DATA_JSON = "csp_ira_aggregated_prediction.json"
II_CRP_DATA_PATH = os.path.join(TITLE_II_DATA_PATH, "programs", "crp")
CRP_STATE_DISTRIBUTION_DATA_JSON = "crp_state_distribution_data.json"
CRP_SUBPROGRAMS_DATA_JSON = "crp_subprograms_data.json"
II_ACEP_DATA_PATH = os.path.join(TITLE_II_DATA_PATH, "programs", "acep")
ACEP_STATE_DISTRIBUTION_DATA_JSON = "acep_state_distribution_data.json"
ACEP_SUBPROGRAMS_DATA_JSON = "acep_subprograms_data.json"
II_RCPP_DATA_PATH = os.path.join(TITLE_II_DATA_PATH, "programs", "rcpp")
RCPP_STATE_DISTRIBUTION_DATA_JSON = "rcpp_state_distribution_data.json"
RCPP_SUBPROGRAMS_DATA_JSON = "rcpp_subprograms_data.json"
II_PROPOSALS_2024_HOUSE_EQIP_DATA_PATH = os.path.join(TITLE_II_DATA_PATH, "proposals", "2024", "house", "eqip")
HOUSE_PREDICTED_DATA_JSON = "house_outlay_max.json"
HOUSE_PREDICTED_PRACTICE_CATEGORIES_DATA_JSON = "house_outlay_practices.json"
TITLE_IV_DATA_PATH = os.path.join("controllers", "data", "title-iv")
IV_SNAP_DATA_PATH = os.path.join(TITLE_IV_DATA_PATH, "programs", "snap")

TITLE_XI_DATA_PATH = os.path.join("controllers", "data", "title-xi")
XI_CROP_INS_DATA_PATH = os.path.join(TITLE_XI_DATA_PATH, "programs", "crop-insurance")
CROP_INSURANCE_SUMMARY_DATA_JSON = "crop_insurance_subprograms_data.json"
CROP_INSURANCE_STATE_DISTRIBUTION_DATA_JSON = "crop_insurance_state_distribution_data.json"

TITLE_I_NAME = "Title I: Commodities"
TITLE_II_NAME = "Title II: Conservation"
TITLE_IV_NAME = "Title IV: Nutrition"
TITLE_XI_NAME = "Title XI: Crop Insurance"

TITLE_I_SUBTITLE_A_NAME = "Total Commodities Programs, Subtitle A"
TITLE_I_SUBTITLE_D_NAME = "Dairy Margin Coverage, Subtitle D"
TITLE_I_SUBTITLE_E_NAME = "Supplemental Agricultural Disaster Assistance, Subtitle E"
TITLE_II_EQIP_PROGRAM_NAME = "Environmental Quality Incentives Program (EQIP)"
TITLE_II_CSP_PROGRAM_NAME = "Conservation Stewardship Program (CSP)"
TITLE_II_CRP_PROGRAM_NAME = "Conservation Reserve Program (CRP)"
TITLE_II_ACEP_PROGRAM_NAME = "Agricultural Conservation Easement Program (ACEP)"
TITLE_II_RCPP_PROGRAM_NAME = "Regional Conservation Partnership Program (RCPP)"
TITLE_IV_SNAP_PROGRAM_NAME = "Supplemental Nutrition Assistance Program (SNAP)"
TITLE_XI_CROP_INSURANCE_PROGRAM_NAME = "Crop Insurance"

def search():
    out_json = jsonutils.create_test_message()

    return out_json


# GET all the entries from summary table
def summary_search():
    endpoint_response = generate_summary_response(cfg.ALL_PROGRAMS_START_YEAR, cfg.ALL_PROGRAMS_END_YEAR)
    return endpoint_response


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
    endpoint_response = generate_allprograms_response(cfg.ALL_PROGRAMS_START_YEAR, cfg.ALL_PROGRAMS_END_YEAR)
    return endpoint_response


# /pdl/titles/title-i/summary:
def titles_title_i_summary_search():
    min_year, max_year = cfg.TITLE_I_START_YEAR, cfg.TITLE_I_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)
    title_id = 100

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Return all data if invalid range

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_i_total_summary_response(title_id, start_year, end_year)
    return endpoint_response


# /pdl/titles/title-i/state-distribution:
def titles_title_i_state_distribution_search():
    min_year, max_year = cfg.TITLE_I_START_YEAR, cfg.TITLE_I_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)
    title_id = 100

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Reset to full range if invalid

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_i_total_state_distribution_response(title_id, start_year, end_year)
    return endpoint_response


# /pdl/titles/title-i/subtitles/subtitle-a/map:
def titles_title_i_subtitles_subtitle_a_map_search():
    # set the file path
    subtitle_data = os.path.join(I_SUBTITLE_A_DATA_PATH, COMMOD_MAP_DATA_JSON)

    # open file
    with open(subtitle_data, 'r') as map_data:
        file_data = map_data.read()

    # parse file
    data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

    return data_json


# /pdl/titles/title-i/subtitles/subtitle-a/state-distribution:
def titles_title_i_subtitles_subtitle_a_state_distribution_search():
    subtitle_id = get_subtitle_id(TITLE_I_SUBTITLE_A_NAME)
    if subtitle_id is None:
        msg = {
            "reason": "No record for the given subtitle name " + TITLE_I_SUBTITLE_A_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("Subtitle A: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    min_year, max_year = cfg.TITLE_I_START_YEAR, cfg.TITLE_I_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Reset to full range if invalid

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_i_state_distribution_response(subtitle_id, start_year, end_year)
    return endpoint_response


# /pdl/titles/title-i/subtitles/subtitle-a/summary:
def titles_title_i_subtitles_subtitle_a_summary_search():
    subtitle_id = get_subtitle_id(TITLE_I_SUBTITLE_A_NAME)
    if subtitle_id is None:
        msg = {
            "reason": "No record for the given subtitle name " + TITLE_I_SUBTITLE_A_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("Subtitle A: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    min_year, max_year = cfg.TITLE_I_START_YEAR, cfg.TITLE_I_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Reset to full range if invalid

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_i_summary_response(subtitle_id, start_year, end_year)
    return endpoint_response


# /pdl/titles/title-i/subtitles/subtitle-d/state-distribution:
def titles_title_i_subtitles_subtitle_d_state_distribution_search():
    subtitle_id = get_subtitle_id(TITLE_I_SUBTITLE_D_NAME)
    if subtitle_id is None:
        msg = {
            "reason": "No record for the given subtitle name " + TITLE_I_SUBTITLE_D_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("Subtitle D: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    min_year, max_year = cfg.TITLE_I_START_YEAR, cfg.TITLE_I_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Reset to full range if invalid

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_i_state_distribution_response(subtitle_id, start_year, end_year)
    return endpoint_response


# /pdl/titles/title-i/subtitles/subtitle-d/summary:
def titles_title_i_subtitles_subtitle_d_summary_search():
    subtitle_id = get_subtitle_id(TITLE_I_SUBTITLE_D_NAME)
    if subtitle_id is None:
        msg = {
            "reason": "No record for the given subtitle name " + TITLE_I_SUBTITLE_D_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("Subtitle D: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    min_year, max_year = cfg.TITLE_I_START_YEAR, cfg.TITLE_I_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Reset to full range if invalid

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_i_summary_response(subtitle_id, start_year, end_year)
    return endpoint_response


# /pdl/titles/title-i/subtitles/subtitle-e/state-distribution:
def titles_title_i_subtitles_subtitle_e_state_distribution_search():
    subtitle_id = get_subtitle_id(TITLE_I_SUBTITLE_E_NAME)
    if subtitle_id is None:
        msg = {
            "reason": "No record for the given subtitle name " + TITLE_I_SUBTITLE_E_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("Subtitle E: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    min_year, max_year = cfg.TITLE_I_START_YEAR, cfg.TITLE_I_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Reset to full range if invalid

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_i_state_distribution_response(subtitle_id, start_year, end_year)
    return endpoint_response


# /pdl/titles/title-i/subtitles/subtitle-e/summary:
def titles_title_i_subtitles_subtitle_e_summary_search():
    subtitle_id = get_subtitle_id(TITLE_I_SUBTITLE_E_NAME)
    if subtitle_id is None:
        msg = {
            "reason": "No record for the given subtitle name " + TITLE_I_SUBTITLE_E_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("Subtitle E: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    min_year, max_year = cfg.TITLE_I_START_YEAR, cfg.TITLE_I_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Reset to full range if invalid

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_i_summary_response(subtitle_id, start_year, end_year)
    return endpoint_response


# /pdl/titles/title-i/subtitles/subtitle-a/arc-plc-payments/current
def titles_title_i_subtitles_subtitle_a_arc_plc_payments_current_search():
    # set the file path
    arc_plc_current_data = os.path.join(I_SUBTITLE_A_DATA_PATH, ARC_PLC_DATA_JSON)

    with open(arc_plc_current_data, 'rb') as current_data:
        file_data = current_data.read()

    response = Response(file_data, mimetype='application/json')
    response.headers['Content-Encoding'] = 'gzip'
    return response

# /pdl/titles/title-i/subtitles/subtitle-a/arc-plc-payments/baseline
def titles_title_i_subtitles_subtitle_a_arc_plc_payments_baseline_search():
    # set the file path
    arc_plc_current_obbba_data = os.path.join(I_SUBTITLE_A_DATA_PATH, ARC_PLC_CURRENT_OBBBA_DATA_JSON)

    with open(arc_plc_current_obbba_data, 'rb') as current_obbba_data:
        file_data = current_obbba_data.read()

    response = Response(file_data, mimetype='application/json')
    response.headers['Content-Encoding'] = 'gzip'
    return response

# /pdl/titles/title-i/subtitles/subtitle-a/arc-plc-payments/obbba
def titles_title_i_subtitles_subtitle_a_arc_plc_payments_obbba_search():
    # set the file path
    arc_plc_proposed_obbba_data = os.path.join(I_PROPOSALS_SUBTITLE_A_DATA_PATH, ARC_PLC_PROPOSED_OBBBA_DATA_JSON)

    with open(arc_plc_proposed_obbba_data, 'rb') as proposed_obbba_data:
        file_data = proposed_obbba_data.read()

    response = Response(file_data, mimetype='application/json')
    response.headers['Content-Encoding'] = 'gzip'
    return response

# /pdl/titles/title-i/subtitles/subtitle-a/arc-plc-payments/proposed
def titles_title_i_subtitles_subtitle_a_arc_plc_payments_proposed_search():
    # set the file path
    arc_plc_proposed_data = os.path.join(I_PROPOSALS_SUBTITLE_A_DATA_PATH, ARC_PLC_PROPOSAL_DATA_JSON)

    with open(arc_plc_proposed_data, 'rb') as proposed_data:
        file_data = proposed_data.read()

    response = Response(file_data, mimetype='application/json')
    response.headers['Content-Encoding'] = 'gzip'
    return response


# /pdl/titles/title-ii/summary:
def titles_title_ii_summary_search():
    min_year, max_year = cfg.TITLE_II_START_YEAR, cfg.TITLE_II_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    title_id = get_title_id(TITLE_II_NAME)
    if title_id is None:
        msg = {
            "reason": "No record for the given title name " + TITLE_II_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("Title II: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Return all data if invalid range

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_ii_total_summary_response(title_id, start_year, end_year)

    return endpoint_response


# /pdl/titles/title-ii/state-distribution:
def titles_title_ii_state_distribution_search():
    min_year, max_year = cfg.TITLE_II_START_YEAR, cfg.TITLE_II_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    title_id = get_title_id(TITLE_II_NAME)
    if title_id is None:
        msg = {
            "reason": "No record for the given title name " + TITLE_II_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("Title II: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Return all data if invalid range

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_ii_total_state_distribution_response(title_id, start_year, end_year)

    return endpoint_response

# /pdl/titles/title-ii/programs/eqip/map
def titles_title_ii_programs_eqip_map_search():
    # set the file path
    eqip_data = os.path.join(II_EQIP_DATA_PATH, EQIP_MAP_DATA_JSON)

    # open file
    with open(eqip_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-ii/programs/eqip/state-distribution
def titles_title_ii_programs_eqip_state_distribution_search(practice_code=None):
    min_year, max_year = cfg.TITLE_II_START_YEAR, cfg.TITLE_II_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    program_id = get_program_id(TITLE_II_EQIP_PROGRAM_NAME)
    if program_id is None:
        msg = {
            "reason": "No record for the given program name " + TITLE_II_EQIP_PROGRAM_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("EQIP: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Return all data if invalid range

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_ii_state_distribution_response(program_id, start_year, end_year, practice_code=practice_code)

    return endpoint_response


# /pdl/titles/title-ii/programs/eqip/summary
def titles_title_ii_programs_eqip_summary_search():
    min_year, max_year = cfg.TITLE_II_START_YEAR, cfg.TITLE_II_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    program_id = get_program_id(TITLE_II_EQIP_PROGRAM_NAME)
    if program_id is None:
        msg = {
            "reason": "No record for the given program name " + TITLE_II_EQIP_PROGRAM_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("EQIP: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Return all data if invalid range

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_ii_summary_response(program_id, start_year, end_year)

    return endpoint_response


# /pdl/titles/title-ii/programs/eqip/practice-names
def titles_title_ii_programs_eqip_practice_names_search():
    min_year, max_year = cfg.TITLE_II_START_YEAR, cfg.TITLE_II_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    program_id = get_program_id(TITLE_II_EQIP_PROGRAM_NAME)
    if program_id is None:
        msg = {
            "reason": "No record for the given program name " + TITLE_II_EQIP_PROGRAM_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("EQIP: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Return all data if invalid range

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year


    endpoint_response = generate_title_ii_practice_names_response(program_id, start_year, end_year)

    return endpoint_response


# /pdl/titles/title-ii/programs/eqip-ira/state-distribution
def titles_title_ii_programs_eqip_ira_state_distribution_search():
    # set the file path
    eqip_ira_data = os.path.join(II_EQIP_IRA_DATA_PATH, EQIP_IRA_STATE_DISTRIBUTION_DATA_JSON)

    # open file
    with open(eqip_ira_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-ii/programs/eqip-ira/summary
def titles_title_ii_programs_eqip_ira_summary_search():
    # set the file path
    eqip_ira_data = os.path.join(II_EQIP_IRA_DATA_PATH, EQIP_IRA_SUMMARY_DATA_JSON)

    # open file
    with open(eqip_ira_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-ii/programs/eqip-ira/practice-names
def titles_title_ii_programs_eqip_ira_practice_names_search():
    # set the file path
    eqip_ira_data = os.path.join(II_EQIP_IRA_DATA_PATH, EQIP_IRA_PRACTICE_CATEGORIES_DATA_JSON)

    # open file
    with open(eqip_ira_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-ii/programs/eqip-ira/predicted
def titles_title_ii_programs_eqip_ira_predicted_search():
    # set the file path
    eqip_ira_data = os.path.join(II_EQIP_IRA_DATA_PATH, EQIP_IRA_AGGREGATE_DATA_JSON)

    # open file
    with open(eqip_ira_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-ii/programs/csp/map
def titles_title_ii_programs_csp_map_search():
    # set the file path
    csp_data = os.path.join(II_CSP_DATA_PATH, CSP_MAP_DATA_JSON)

    # open file
    with open(csp_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-ii/programs/csp/state-distribution
def titles_title_ii_programs_csp_state_distribution_search(practice_code=None):
    min_year, max_year = cfg.TITLE_II_START_YEAR, cfg.TITLE_II_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    program_id = get_program_id(TITLE_II_CSP_PROGRAM_NAME)
    if program_id is None:
        msg = {
            "reason": "No record for the given program name " + TITLE_II_CSP_PROGRAM_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("CSP: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Return all data if invalid range

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_ii_state_distribution_response(program_id, start_year, end_year, practice_code=practice_code)

    return endpoint_response


# /pdl/titles/title-ii/programs/csp/summary
def titles_title_ii_programs_csp_summary_search():
    min_year, max_year = cfg.TITLE_II_START_YEAR, cfg.TITLE_II_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    program_id = get_program_id(TITLE_II_CSP_PROGRAM_NAME)
    if program_id is None:
        msg = {
            "reason": "No record for the given program name " + TITLE_II_CSP_PROGRAM_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("CSP: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Return all data if invalid range

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_ii_summary_response(program_id, start_year, end_year)

    return endpoint_response


# /pdl/titles/title-ii/programs/eqip/practice-names
def titles_title_ii_programs_csp_practice_names_search():
    min_year, max_year = cfg.TITLE_II_START_YEAR, cfg.TITLE_II_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    program_id = get_program_id(TITLE_II_CSP_PROGRAM_NAME)
    if program_id is None:
        msg = {
            "reason": "No record for the given program name " + TITLE_II_CSP_PROGRAM_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("EQIP: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Return all data if invalid range

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_ii_practice_names_response(program_id, start_year, end_year)

    return endpoint_response


# /pdl/titles/title-ii/programs/csp_ira/state-distribution
def titles_title_ii_programs_csp_ira_state_distribution_search():
    # set the file path
    csp_ira_data = os.path.join(II_CSP_IRA_DATA_PATH, CSP_IRA_STATE_DISTRIBUTION_DATA_JSON)

    # open file
    with open(csp_ira_data, 'r') as state_distribution_data:
        file_data = state_distribution_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-ii/programs/csp-ira/summary
def titles_title_ii_programs_csp_ira_summary_search():
    # set the file path
    csp_ira_data = os.path.join(II_CSP_IRA_DATA_PATH, CSP_IRA_SUMMARY_DATA_JSON)

    # open file
    with open(csp_ira_data, 'r') as summary_data:
        file_data = summary_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-ii/programs/csp-ira/practice-names
def titles_title_ii_programs_csp_ira_practice_names_search():
    # set the file path
    csp_ira_data = os.path.join(II_CSP_IRA_DATA_PATH, CSP_IRA_PRACTICE_CATEGORIES_DATA_JSON)

    # open file
    with open(csp_ira_data, 'r') as practice_data:
        file_data = practice_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-ii/programs/csp-ira/predicted
def titles_title_ii_programs_csp_ira_predicted_search():
    # set the file path
    csp_ira_data = os.path.join(II_CSP_IRA_DATA_PATH, CSP_IRA_AGGREGATE_DATA_JSON)

    # open file
    with open(csp_ira_data, 'r') as predicted_data:
        file_data = predicted_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-ii/programs/crp/state-distribution
def titles_title_ii_programs_crp_state_distribution_search():
    min_year, max_year = cfg.TITLE_II_START_YEAR, cfg.TITLE_II_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    program_id = get_program_id(TITLE_II_CRP_PROGRAM_NAME)
    if program_id is None:
        msg = {
            "reason": "No record for the given program name " + TITLE_II_CRP_PROGRAM_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("CRP: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Return all data if invalid range

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_ii_state_distribution_response(program_id, start_year, end_year)

    return endpoint_response


# /pdl/titles/title-ii/programs/crp/summary
def titles_title_ii_programs_crp_summary_search():
    min_year, max_year = cfg.TITLE_II_START_YEAR, cfg.TITLE_II_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    program_id = get_program_id(TITLE_II_CRP_PROGRAM_NAME)
    if program_id is None:
        msg = {
            "reason": "No record for the given program name " + TITLE_II_CRP_PROGRAM_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("CRP: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Return all data if invalid range

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_ii_summary_response(program_id, start_year, end_year)

    return endpoint_response


# /pdl/titles/title-ii/programs/acep/state-distribution
def titles_title_ii_programs_acep_state_distribution_search():
    min_year, max_year = cfg.TITLE_II_START_YEAR, cfg.TITLE_II_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    program_id = get_program_id(TITLE_II_ACEP_PROGRAM_NAME)
    if program_id is None:
        msg = {
            "reason": "No record for the given program name " + TITLE_II_ACEP_PROGRAM_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("ACEP: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Return all data if invalid range

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_ii_state_distribution_response(program_id, start_year, end_year)
    return endpoint_response


# /pdl/titles/title-ii/programs/acep/summary
def titles_title_ii_programs_acep_summary_search():
    min_year, max_year = cfg.TITLE_II_START_YEAR, cfg.TITLE_II_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    program_id = get_program_id(TITLE_II_ACEP_PROGRAM_NAME)
    if program_id is None:
        msg = {
            "reason": "No record for the given program name " + TITLE_II_ACEP_PROGRAM_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("ACEP: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Return all data if invalid range

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_ii_summary_response(program_id, start_year, end_year)
    return endpoint_response


# /pdl/titles/title-ii/programs/rcpp/state-distribution
def titles_title_ii_programs_rcpp_state_distribution_search():
    min_year, max_year = cfg.TITLE_II_START_YEAR, cfg.TITLE_II_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    program_id = get_program_id(TITLE_II_RCPP_PROGRAM_NAME)
    if program_id is None:
        msg = {
            "reason": "No record for the given program name " + TITLE_II_RCPP_PROGRAM_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("RCPP: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Return all data if invalid range

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_ii_state_distribution_response(program_id, start_year, end_year)
    return endpoint_response


# /pdl/titles/title-ii/programs/rcpp/summary
def titles_title_ii_programs_rcpp_summary_search():
    min_year, max_year = cfg.TITLE_II_START_YEAR, cfg.TITLE_II_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    program_id = get_program_id(TITLE_II_RCPP_PROGRAM_NAME)
    if program_id is None:
        msg = {
            "reason": "No record for the given program name " + TITLE_II_RCPP_PROGRAM_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("RCPP: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Return all data if invalid range

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_ii_summary_response(program_id, start_year, end_year)

    return endpoint_response

# /pdl/titles/title-ii/proposals/2024/house/eqip/predicted
def titles_title_ii_proposals_2024_house_eqip_predicted_search():
    # set the file path
    house_outlay_data = os.path.join(II_PROPOSALS_2024_HOUSE_EQIP_DATA_PATH, HOUSE_PREDICTED_DATA_JSON)

    # open file
    with open(house_outlay_data, 'r') as predicted_data:
        file_data = predicted_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-ii/proposals/2024/house/eqip/practice-names
def titles_title_ii_proposals_2024_house_eqip_practice_names_search():
    # set the file path
    house_outlay_data = os.path.join(II_PROPOSALS_2024_HOUSE_EQIP_DATA_PATH, HOUSE_PREDICTED_PRACTICE_CATEGORIES_DATA_JSON)

    # open file
    with open(house_outlay_data, 'r') as practice_data:
        file_data = practice_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-xi/programs/crop-insurance/state-distribution
def titles_title_xi_programs_crop_insurance_state_distribution_search():
    program_id = get_program_id(TITLE_XI_CROP_INSURANCE_PROGRAM_NAME)
    if program_id is None:
        msg = {
            "reason": "No record for the given program name " + TITLE_XI_CROP_INSURANCE_PROGRAM_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("Crop Insurance: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    min_year, max_year = cfg.CROP_INSURANCE_START_YEAR, cfg.CROP_INSURANCE_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Reset to full range if invalid

    if start_year is None:
        start_year = min_year  # Default to the earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_xi_state_distribution_response(program_id, start_year, end_year)
    return endpoint_response


# /pdl/titles/title-xi/programs/crop-insurance/summary
def titles_title_xi_programs_crop_insurance_summary_search():
    program_id = get_program_id(TITLE_XI_CROP_INSURANCE_PROGRAM_NAME)
    if program_id is None:
        msg = {
            "reason": "No record for the given program name " + TITLE_XI_CROP_INSURANCE_PROGRAM_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("Crop Insurance: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    min_year, max_year = cfg.CROP_INSURANCE_START_YEAR, cfg.CROP_INSURANCE_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Reset to full range if invalid

    if start_year is None:
        start_year = min_year  # Default to the earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_xi_summary_response(program_id, start_year, end_year)
    return endpoint_response

# /pdl/titles/title-iv/programs/snap/state-distribution
def titles_title_iv_programs_snap_state_distribution_search():
    program_id = get_program_id(TITLE_IV_SNAP_PROGRAM_NAME)
    if program_id is None:
        msg = {
            "reason": "No record for the given program name " + TITLE_IV_SNAP_PROGRAM_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("SNAP: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    min_year, max_year = cfg.SNAP_START_YEAR, cfg.SNAP_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Reset to full range if invalid

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_iv_state_distribution_response(program_id, start_year, end_year)
    return endpoint_response

# /pdl/titles/title-iv/programs/snap/summary
def titles_title_iv_programs_snap_summary_search():
    program_id = get_program_id(TITLE_IV_SNAP_PROGRAM_NAME)
    if program_id is None:
        msg = {
            "reason": "No record for the given program name " + TITLE_IV_SNAP_PROGRAM_NAME,
            "error": "Not found: " + request.url,
        }
        logging.error("SNAP: " + json.dumps(msg))
        return rs_handlers.not_found(msg)

    min_year, max_year = cfg.SNAP_START_YEAR, cfg.SNAP_END_YEAR
    start_year = request.args.get('start_year', type=int, default=min_year)
    end_year = request.args.get('end_year', type=int, default=max_year)

    if start_year and end_year and start_year > end_year:
        start_year, end_year = min_year, max_year  # Reset to full range if invalid

    if start_year is None:
        start_year = min_year  # Default to earliest available year

    if end_year is None:
        end_year = max_year  # Default to latest available year

    endpoint_response = generate_title_iv_summary_response(program_id, start_year, end_year)
    return endpoint_response

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


def get_title_id(title_name):
    session = Session()
    title = session.query(Title).filter_by(name=title_name).first()
    if title is None:
        return None
    return title.id


def get_subtitle_id(subtitle_name):
    session = Session()
    subtitle = session.query(Subtitle).filter_by(name=subtitle_name).first()
    if subtitle is None:
        return None
    return subtitle.id


def get_program_id(program_name):
    session = Session()
    program = session.query(Program).filter_by(name=program_name).first()
    if program is None:
        return None
    return program.id


def generate_allprograms_response(start_year, end_year):
    session = Session()

    try:
        # Building the SQL query dynamically
        year_columns = []

        for year in range(start_year, end_year + 1):
            year_columns.append(f"""
            SUM(CASE WHEN t.name = 'Title I: Commodities' AND p.year = {year} THEN p.payment ELSE 0 END) AS "Title I {year}",
            SUM(CASE WHEN t.name = 'Title II: Conservation' AND p.year = {year} AND (sub_program_id IN (SELECT id FROM pdl.sub_programs WHERE pdl.sub_programs.name = 'Total CRP') OR sub_program_id IS NULL) THEN p.payment ELSE 0 END) AS "Title II {year}",
            SUM(CASE WHEN t.name = 'Title IV: Nutrition' AND p.year = {year} THEN p.payment ELSE 0 END) AS "SNAP {year}",
            SUM(CASE WHEN t.name = 'Title IX: Crop Insurance' AND p.year = {year} THEN p.net_farmer_benefit_amount ELSE 0 END) AS "Crop Insurance {year}",
            SUM(CASE WHEN p.year = {year} AND (sub_program_id IN (SELECT id FROM pdl.sub_programs WHERE pdl.sub_programs.name IN ('Total CRP', 'Agriculture Risk Coverage County Option (ARC-CO)', 'Agriculture Risk Coverage Individual Coverage (ARC-IC)')) OR sub_program_id IS NULL) THEN COALESCE(p.payment, 0) + COALESCE(p.net_farmer_benefit_amount, 0) ELSE 0 END) AS "{year} All Programs Total"
            """)

        # Add the totals for each program and the overall total
        totals = f"""
        SUM(CASE WHEN t.name = 'Title I: Commodities' AND p.year BETWEEN {start_year} AND {end_year} THEN p.payment ELSE 0 END) AS "Title I Total",
        SUM(CASE WHEN t.name = 'Title II: Conservation' AND p.year BETWEEN {start_year} AND {end_year} AND (sub_program_id IN (SELECT id FROM pdl.sub_programs WHERE pdl.sub_programs.name = 'Total CRP') OR sub_program_id IS NULL) THEN p.payment ELSE 0 END) AS "Title II Total",
        SUM(CASE WHEN t.name = 'Title IV: Nutrition' AND p.year BETWEEN {start_year} AND {end_year} THEN p.payment ELSE 0 END) AS "SNAP Total",
        SUM(CASE WHEN t.name = 'Title IX: Crop Insurance' AND p.year BETWEEN {start_year} AND {end_year} THEN p.net_farmer_benefit_amount ELSE 0 END) AS "Crop Insurance Total",
        SUM(CASE WHEN (sub_program_id IN (SELECT id FROM pdl.sub_programs WHERE pdl.sub_programs.name IN ('Total CRP', 'Agriculture Risk Coverage County Option (ARC-CO)', 'Agriculture Risk Coverage Individual Coverage (ARC-IC)')) OR sub_program_id IS NULL) THEN COALESCE(p.payment, 0) + COALESCE(p.net_farmer_benefit_amount, 0) ELSE 0 END) AS "{str(start_year)[-2:]}-{str(end_year)[-2:]} All Programs Total"
        """

        # Combine the query of non-dynamic part
        sql_query = f"""
        SELECT
            p.state_code AS "State",
            {','.join(year_columns)},
            {totals}
        FROM
            pdl.payments p
        JOIN
            pdl.titles t ON p.title_id = t.id
        GROUP BY
            p.state_code
        ORDER BY
            p.state_code;
        """

        result = session.execute(text(sql_query))

        columns = result.keys()

        state_data = []
        total_row = {"State": "Total"}
        start_to_end_years_total_key = str(start_year)[-2:] + "-" + str(end_year)[-2:] + " All Programs Total"

        # Initialize total_row with zero values for all keys in the desired order
        for year in range(start_year, end_year + 1):
            total_row[f"Title I {year}"] = 0
        total_row["Title I Total"] = 0

        for year in range(start_year, end_year + 1):
            total_row[f"Title II {year}"] = 0
        total_row["Title II Total"] = 0

        for year in range(start_year, end_year + 1):
            total_row[f"Crop Insurance {year}"] = 0
        total_row["Crop Insurance Total"] = 0

        for year in range(start_year, end_year + 1):
            total_row[f"SNAP {year}"] = 0
        total_row["SNAP Total"] = 0

        for year in range(start_year, end_year + 1):
            total_row[f"{year} All Programs Total"] = 0
        total_row[start_to_end_years_total_key] = 0

        for row in result:
            result_dict = dict(zip(columns, row))  # Using zip() to match columns with their values

            # Initialize the formatted result with the state
            formatted_result = {
                "State": result_dict.get("State")
            }

            # Add Title I data for all years in the correct order
            for year in range(start_year, end_year + 1):
                value = result_dict.get(f"Title I {year}", 0)
                formatted_result[f"Title I {year}"] = value
                total_row[f"Title I {year}"] += value

            # Add Title I Total
            formatted_result["Title I Total"] = result_dict.get("Title I Total", 0)
            total_row["Title I Total"] += formatted_result["Title I Total"]

            # Add Title II data for all years
            for year in range(start_year, end_year + 1):
                value = result_dict.get(f"Title II {year}", 0)
                formatted_result[f"Title II {year}"] = value
                total_row[f"Title II {year}"] += value

            # Add Title II Total
            formatted_result["Title II Total"] = result_dict.get("Title II Total", 0)
            total_row["Title II Total"] += formatted_result["Title II Total"]

            # Add Crop Insurance data for all years
            for year in range(start_year, end_year + 1):
                value = result_dict.get(f"Crop Insurance {year}", 0)
                formatted_result[f"Crop Insurance {year}"] = value
                total_row[f"Crop Insurance {year}"] += value

            # Add Crop Insurance Total
            formatted_result["Crop Insurance Total"] = result_dict.get("Crop Insurance Total", 0)
            total_row["Crop Insurance Total"] += formatted_result["Crop Insurance Total"]

            # Add SNAP data for all years
            for year in range(start_year, end_year + 1):
                value = result_dict.get(f"SNAP {year}", 0)
                formatted_result[f"SNAP {year}"] = value
                total_row[f"SNAP {year}"] += value

            # Add SNAP Total
            formatted_result["SNAP Total"] = result_dict.get("SNAP Total", 0)
            total_row["SNAP Total"] += formatted_result["SNAP Total"]

            # Add the all programs total for each year
            for year in range(start_year, end_year + 1):
                value = result_dict.get(f"{year} All Programs Total", 0)
                formatted_result[f"{year} All Programs Total"] = value
                total_row[f"{year} All Programs Total"] += value

            # Add the final total for all programs between the years
            formatted_result[start_to_end_years_total_key] = result_dict.get(start_to_end_years_total_key, 0)

            # Append the formatted result to the state data
            state_data.append(formatted_result)

        # Add the final total for all programs between the years
        for year in range(start_year, end_year + 1):
            total_row[start_to_end_years_total_key] += total_row[f"{year} All Programs Total"]

        # Append the total row at the end of state data
        state_data.append(total_row)

        return state_data

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return {"error": str(e)}

    finally:
        session.close()


def generate_summary_response(start_year, end_year):
    session = Session()

    try:
        # Generate dynamic SQL query to fetch the summary, ensuring sums are correctly applied
        query = f"""
        SELECT
            t.name AS "Title",
            p.state_code AS "State",
            p.year AS "Fiscal Year",
            SUM(COALESCE(p.payment, 0) + COALESCE(p.net_farmer_benefit_amount, 0)) AS "Amount",
            SUM(COALESCE(p.recipient_count, 0)) AS "Average Monthly Participation"
        FROM
            pdl.payments p
        JOIN
            pdl.titles t ON p.title_id = t.id
        LEFT JOIN
            pdl.sub_programs sp ON p.sub_program_id = sp.id
        WHERE
            p.year BETWEEN {start_year} AND {end_year}
            AND (sp.name IN ('Total CRP', 'Agriculture Risk Coverage County Option (ARC-CO)', 'Agriculture Risk Coverage Individual Coverage (ARC-IC)') OR p.sub_program_id IS NULL)
        GROUP BY
            t.name, p.state_code, p.year
        ORDER BY
            CASE
                WHEN t.name = 'Title I: Commodities' THEN 1
                WHEN t.name = 'Title II: Conservation' THEN 2
                WHEN t.name = 'Title IX: Crop Insurance' THEN 3
                WHEN t.name = 'Title IV: Nutrition' THEN 4
            END,
            p.year,
            p.state_code;
        """

        # Execute the query
        result = session.execute(text(query))

        # Fetch column names from the result set
        columns = result.keys()

        # Map titles to desired names
        title_mapping = {
            "Title IV: Nutrition": "Supplemental Nutrition Assistance Program (SNAP)",
            "Title IX: Crop Insurance": "Crop Insurance"
        }

        # Process the result into a dictionary format
        summary_data = []
        for row in result:
            result_dict = dict(zip(columns, row))  # Using zip() to match columns with their values

            # Get the title and apply the mapping if it exists
            title = result_dict.get("Title")
            mapped_title = title_mapping.get(title, title)

            # Format each entry in the desired summary structure, using `recipient_count` for Average Monthly Participation
            formatted_entry = {
                "Title": mapped_title,
                "State": result_dict.get("State"),
                "Fiscal Year": result_dict.get("Fiscal Year"),
                "Amount": result_dict.get("Amount"),
                "Average Monthly Participation": result_dict.get("Average Monthly Participation") if result_dict.get("Average Monthly Participation") else ""
            }

            # Append the formatted entry to the summary data
            summary_data.append(formatted_entry)

        # Return the formatted summary data as JSON
        return summary_data

    except Exception as e:
        # Log any errors that occur
        logging.error(f"Error occurred: {str(e)}")
        return {"error": str(e)}

    finally:
        # Close the session
        session.close()


def generate_title_iv_state_distribution_response(program_id, start_year, end_year):
    session = Session()

    # construct the query
    program_query = session.query(
        Payment.state_code.label('state'),
        Program.name.label('programName'),
        Payment.year.label('year'),
        Payment.payment.label('totalPaymentInDollars'),
        Payment.recipient_count.label('totalCounts')
    ).join(
        Program, Payment.program_id == Program.id
    ).filter(
        Payment.program_id == program_id,
        Payment.year.between(start_year, end_year)
    )

    # execute the query
    program_result = program_query.all()

    # create dictionaries
    program_response_dict = defaultdict(list)
    year_dict = defaultdict(list)
    total_national_payment_dict = defaultdict(float)
    total_national_average_monthly_participation_dict = defaultdict(int)

    # aggregate data
    for record in program_result:
        year = str(record[2])
        state = record[0]
        payment = record[3]
        recipient_count = record[4]

        year_dict[year].append({
            'state': state,
            'totalPaymentInDollars': payment,
            'averageMonthlyParticipation': recipient_count
        })

        # update total national payment and count for the year
        total_national_payment_dict[year] += payment
        total_national_average_monthly_participation_dict[year] += recipient_count

    # create output response dictionary
    for year, data in year_dict.items():
        program_response_dict[year] = []
        for item in data:
            state = item['state']
            total_payment = item['totalPaymentInDollars']
            average_participation = item['averageMonthlyParticipation']

            total_payment_percentage = (total_payment / total_national_payment_dict[year]) * 100
            average_participation_percentage = (average_participation / total_national_average_monthly_participation_dict[year]) * 100

            program_response_dict[year].append({
                'state': state,
                'totalPaymentInDollars': total_payment,
                'totalPaymentInPercentageNationwide': round(total_payment_percentage, 2),
                'averageMonthlyParticipation': average_participation,
                'averageMonthlyParticipationInPercentageNationwide': round(average_participation_percentage, 2)
            })

        # sort states by decreasing order of total payment in dollars
        program_response_dict[year] = \
            sorted(program_response_dict[year], key=lambda x: x['totalPaymentInDollars'], reverse=True)

    # calculate total payment and average monthly participation for each state across all years
    state_total_data = defaultdict(lambda: {'totalPaymentInDollars': 0, 'averageMonthlyParticipation': 0})

    for year, data in year_dict.items():
        for item in data:
            state = item['state']
            total_payment = item['totalPaymentInDollars']
            average_participation = item['averageMonthlyParticipation']

            state_total_data[state]['totalPaymentInDollars'] += total_payment
            state_total_data[state]['averageMonthlyParticipation'] += average_participation

    # calculate the sum of total national payment and count for all years
    total_national_payment = sum(total_national_payment_dict.values())
    national_average_monthly_participation_across_years = (sum(total_national_average_monthly_participation_dict.values()))/(end_year - start_year + 1)

    # add the total data for each state to the program_response_dict
    total_states_data = []
    for state, total_data in state_total_data.items():
        total_payment = total_data['totalPaymentInDollars']
        average_monthly_participation = total_data['averageMonthlyParticipation']/(end_year - start_year + 1)

        #  calculate percentage using the total national payment and count across all years
        total_payment_percentage = (total_payment / total_national_payment) * 100
        average_monthly_participation_percentage = (average_monthly_participation / national_average_monthly_participation_across_years) * 100

        # append total data for each state to the list
        total_states_data.append({
            'state': state,
            'totalPaymentInDollars': total_payment,
            'totalPaymentInPercentageNationwide': round(total_payment_percentage, 2),
            'averageMonthlyParticipation': round(average_monthly_participation),
            'averageMonthlyParticipationInPercentageNationwide': round(average_monthly_participation_percentage, 2)
        })

    # Sort the total states data by decreasing order of total payment in dollars
    total_states_data = sorted(total_states_data, key=lambda x: x['totalPaymentInDollars'], reverse=True)

    # Add the total states data to the program_response_dict under the key 'TotalStates'
    program_response_dict[str(start_year) + '-' + str(end_year)] = total_states_data

    return program_response_dict

def generate_title_iv_summary_response(program_id, start_year, end_year):
    session = Session()

    # Construct the query
    program_query = session.query(
        func.avg(Payment.recipient_count).label('averageMonthlyRecipientCount'),
        func.sum(Payment.payment).label('totalPaymentInDollars')
    ).join(
        Program, Payment.program_id == Program.id
    ).filter(
        Payment.program_id == program_id,
        Payment.year.between(start_year, end_year)
    )

    # execute the query
    result = program_query.first()

    # aggregate dictionary for summing
    aggregate_dict = {
        'totalPaymentInDollars': round(result.totalPaymentInDollars, 2),
        'averageMonthlyParticipation': round(result.averageMonthlyRecipientCount, 2)
    }

    return aggregate_dict

def generate_title_i_total_state_distribution_response(title_id, start_year, end_year):
    session = Session()

    # construct the query
    program_query = session.query(
        Payment.state_code.label('state'),
        Subtitle.name.label('subtitleName'),
        Payment.year.label('year'),
        Payment.payment.label('totalPaymentInDollars'),
        Payment.recipient_count.label('totalCounts')).join(
        Subtitle, Payment.subtitle_id == Subtitle.id).filter(
        Payment.title_id == title_id,
        Payment.year.between(start_year, end_year)
    )

    # execute the query
    result = program_query.all()

    # create a nested dictionary to store data by year and state
    data_by_year_and_state = defaultdict(
        lambda: defaultdict(lambda: {'totalPaymentInDollars': 0, 'totalRecipients': 0}))
    all_years_summary = defaultdict(lambda: {'totalPaymentInDollars': 0, 'totalRecipients': 0})

    for record in result:
        state, title_name, year, payments, recipients = record
        entry = data_by_year_and_state[year][state]
        entry['state'] = state
        entry['totalPaymentInDollars'] += payments
        entry['totalRecipients'] += recipients

        # add to all years summary
        summary = all_years_summary[state]
        summary['state'] = state
        summary['totalPaymentInDollars'] += payments
        summary['totalRecipients'] += recipients

    # sort by total payment
    sorted_data_by_year = {}
    for year, states in data_by_year_and_state.items():
        sorted_entries = sorted(states.values(), key=lambda x: x['totalPaymentInDollars'], reverse=True)
        sorted_data_by_year[year] = sorted_entries

    # round the total payment
    for year, states in sorted_data_by_year.items():
        for state in states:
            state['totalPaymentInDollars'] = round(state['totalPaymentInDollars'], 2)

    # all years summary
    sorted_summary = sorted(all_years_summary.values(), key=lambda x: x['totalPaymentInDollars'], reverse=True)

    # round the total payment
    for state in sorted_summary:
        state['totalPaymentInDollars'] = round(state['totalPaymentInDollars'], 2)

    sorted_data_by_year[str(start_year) + '-' + str(end_year)] = sorted_summary

    result_dict = dict(sorted_data_by_year)

    return result_dict

def generate_title_ii_total_state_distribution_response(title_id, start_year, end_year):
    session = Session()

    # construct the query
    program_query = (
        session.query(
            Payment.state_code.label('state'),
            Payment.year.label('year'),
            Payment.payment.label('totalPaymentInDollars')
        ).filter(
            Payment.title_id == title_id,
            Payment.year.between(start_year, end_year),
            # when calculating the title level summaries, only calculate Total CRP (sub_program_id == 102) from CRP (program_id == 108)
            or_(
                and_(
                    Payment.program_id == 108,
                    Payment.sub_program_id == 102
                ),
                Payment.program_id != 108
            )
        )
    )

    # execute the query
    result = program_query.all()

    # create a nested dictionary to store data by year and state
    data_by_year_and_state = defaultdict(
        lambda: defaultdict(lambda: {'totalPaymentInDollars': 0, 'totalRecipients': 0}))
    all_years_summary = defaultdict(lambda: {'totalPaymentInDollars': 0, 'totalRecipients': 0})

    for record in result:
        state, year, payments = record
        entry = data_by_year_and_state[year][state]
        entry['state'] = state
        entry['totalPaymentInDollars'] += payments

        # add to all years summary
        summary = all_years_summary[state]
        summary['state'] = state
        summary['totalPaymentInDollars'] += payments

    # sort by total payment
    sorted_data_by_year = {}
    for year, states in data_by_year_and_state.items():
        sorted_entries = sorted(states.values(), key=lambda x: x['totalPaymentInDollars'], reverse=True)
        sorted_data_by_year[year] = sorted_entries

    # round the total payment
    for year, states in sorted_data_by_year.items():
        for state in states:
            state['totalPaymentInDollars'] = round(state['totalPaymentInDollars'], 2)

    # all years summary
    sorted_summary = sorted(all_years_summary.values(), key=lambda x: x['totalPaymentInDollars'], reverse=True)

    # round the total payment
    for state in sorted_summary:
        state['totalPaymentInDollars'] = round(state['totalPaymentInDollars'], 2)

    sorted_data_by_year[str(start_year) + '-' + str(end_year)] = sorted_summary

    result_dict = dict(sorted_data_by_year)

    return result_dict

def generate_title_i_total_summary_response(title_id, start_year, end_year):
    session = Session()

    # construct the query
    program_query = session.query(
        Payment.state_code.label('state'),
        Title.name.label('titleName'),
        Payment.year.label('year'),
        Payment.payment.label('totalPaymentInDollars'),
        Payment.recipient_count.label('totalCounts'),
        Subtitle.name.label('subtitleName')
    ).join(
        Title, Payment.title_id == Title.id
    ).join(
        Subtitle, Payment.subtitle_id == Subtitle.id
    ).filter(
        Payment.title_id == title_id,
        Payment.year.between(start_year, end_year)
    )

    # execute the query
    results = program_query.all()

    # Initialize dictionaries to store aggregated data
    title_summary = defaultdict(lambda: {
        'totalPaymentInDollars': 0,
        'totalCounts': 0,
        'recipients': [],
        'subtitles': defaultdict(lambda: {
            'totalPaymentInDollars': 0,
            'totalCounts': 0,
            'recipients': []
        })
    })

    # Process each record in the data
    for state, title_name, year, payment, recipients, subtitle in results:
        title_summary[title_name]['totalPaymentInDollars'] += payment
        title_summary[title_name]['totalCounts'] += recipients
        title_summary[title_name]['recipients'].append(recipients)

        # Aggregate subtitle data
        subtitle_dict = title_summary[title_name]['subtitles'][subtitle]
        subtitle_dict['totalPaymentInDollars'] += payment
        subtitle_dict['totalCounts'] += recipients
        subtitle_dict['recipients'].append(recipients)

    # Prepare the final summary
    final_summary = []
    for title, info in title_summary.items():
        average_recipient_count = sum(info['recipients']) / len(info['recipients']) if info['recipients'] else 0
        subtitle_list = []
        total_payment_title = info['totalPaymentInDollars']

        for subtitle_name, subtitle_info in info['subtitles'].items():
            subtitle_avg_recipients = sum(subtitle_info['recipients']) / len(subtitle_info['recipients']) if \
            subtitle_info['recipients'] else 0
            payment_percentage = (subtitle_info[
                                      'totalPaymentInDollars'] / total_payment_title * 100) if total_payment_title else 0
            subtitle_list.append({
                'programName': subtitle_name,
                'totalPaymentInDollars': round(subtitle_info['totalPaymentInDollars'], 2),
                'totalCounts': subtitle_info['totalCounts'],
                'averageRecipientCount': subtitle_avg_recipients,
                'totalPaymentInPercentage': round(payment_percentage, 2)
            })

        title_entry = {
            'titleName': title,
            'totalPaymentInDollars': round(info['totalPaymentInDollars'], 2),
            'totalCounts': info['totalCounts'],
            'averageRecipientCount': round(average_recipient_count, 2),
            'subtitles': subtitle_list
        }
        final_summary.append(title_entry)

    return final_summary


def generate_title_ii_total_summary_response(title_id, start_year, end_year):
    session = Session()

    # construct the query
    program_query = session.query(
        Title.name.label('titleName'),
        Program.name.label('programName'),
        func.sum(Payment.payment).label('programPaymentInDollars')
    ).join(
        Title, Payment.title_id == Title.id
    ).join(
        Program, and_(
            Payment.title_id == Program.title_id,
            Payment.program_id == Program.id
        )
    ).filter(
        Payment.title_id == title_id,
        Payment.year.between(start_year, end_year),
        # When calculating the title level summaries, only calculate Total CRP (sub_program_id == 102) from CRP (program_id == 108)
        or_(
            and_(
                Payment.program_id == 108,
                Payment.sub_program_id == 102
            ),
            Payment.program_id != 108
        )
    ).group_by(
        Payment.title_id,
        Payment.program_id,
        Title.name,
        Program.name
    )

    # execute the query
    results = program_query.all()

    # Process each record in the data
    program_list = []
    title_total_payment = sum(result.programPaymentInDollars for result in results)
    for title_name, program_name, program_payment in results:
        payment_percentage = (program_payment / title_total_payment * 100) if title_total_payment else 0
        program_list.append({
            'programName': program_name,
            'totalPaymentInDollars': program_payment,
            'totalPaymentInPercentage': round(payment_percentage, 2)
        })

    title_name = next(iter(set(result.titleName for result in results)), None) # get the first title name from the result
    title_entry = {
        'titleName': title_name,
        'totalPaymentInDollars': title_total_payment,
        'startYear': start_year,
        'endYear': end_year,
        'programs': program_list
    }

    return title_entry

def generate_title_i_state_distribution_response(subtitle_id, start_year, end_year):
    session = Session()

    # Construct the subquery
    subtitle_subquery = (session.query(func.sum(Payment.payment))
                         .filter(Payment.subtitle_id == subtitle_id, Payment.year.between(start_year, end_year)).scalar_subquery())
    subtitle_subquery_recipient_count = (session.query(func.sum(Payment.recipient_count))
                                         .filter(Payment.subtitle_id == subtitle_id, Payment.year.between(start_year, end_year)).scalar_subquery())

    # Construct the main query
    subtitle_query = session.query(
        Payment.state_code.label('state'),
        Subtitle.name.label('subtitleName'),
        (func.cast(func.sum(Payment.payment) / subtitle_subquery * 100, Numeric(5, 2))).label(
            'totalPaymentInPercentageNationwide'),
        func.sum(Payment.payment).label('totalPaymentInDollars'),
        func.round(func.avg(Payment.base_acres), 2).label('averageAreaInAcres'),
        func.cast(func.avg(Payment.recipient_count), BigInteger).label('averageRecipientCount'),
        func.cast(func.sum(Payment.recipient_count), Integer).label('totalCounts'),
        (func.cast(func.sum(Payment.recipient_count) / subtitle_subquery_recipient_count * 100, Numeric(5, 2))).label(
            'averageRecipientCountInPercentageNationwide')
    ).join(
        Subtitle, Payment.subtitle_id == Subtitle.id
    ).filter(
        Payment.subtitle_id == subtitle_id,
        Payment.year.between(start_year, end_year)
    ).group_by(
        Payment.state_code, Subtitle.name
    ).order_by(
        desc('totalPaymentInPercentageNationwide')
    )
    # Extract the column names
    column_names = [item['name'] for item in subtitle_query.statement.column_descriptions]

    # Execute the query
    result = subtitle_query.all()

    # Build subtitle response dictionary
    subtitle_response_dict = dict()
    for row in result:
        response_dict = dict(zip(column_names, row))

        # Cleanup / renaming attributes
        response_dict["totalCountsInPercentageNationwide"] = response_dict["averageRecipientCountInPercentageNationwide"]
        if response_dict['averageAreaInAcres'] is None:
            response_dict['averageAreaInAcres'] = 0.0
        subtitle_response_dict[response_dict['state']] = response_dict

    # Find all programs under the subtitle
    subtitle = Subtitle.query.filter_by(id=subtitle_id).first()
    programs = Program.query.filter_by(subtitle_id=subtitle.id).all()
    program_ids = [program.id for program in programs]

    # For each program, find the subprograms
    subprograms = []
    for program_id in program_ids:
        subprograms += SubProgram.query.filter_by(program_id=program_id).all()
    subprogram_ids = [subprogram.id for subprogram in subprograms]

    program_response_dict = dict()
    # For each program, find state code, total payment, total payment percentage, average recipient count,
    # and average base acres during the given years
    for program_id in program_ids:

        # Construct the subquery
        program_subquery_total_payment = (session.query(func.sum(Payment.payment))
                                          .filter(Payment.program_id == program_id, Payment.year.between(start_year, end_year))
                                          .label('totalPaymentInDollars'))
        program_subquery_recipient_count = (session.query(func.sum(Payment.recipient_count))
                                            .filter(Payment.program_id == program_id,
                                                    Payment.year.between(start_year, end_year)).scalar_subquery())

        total_years = end_year - start_year + 1  # Use total years to calculate average recipient count

        # Construct the main query
        program_query = session.query(
            Payment.state_code.label('state'),
            Program.name.label('programName'),
            func.sum(Payment.payment).label('totalPaymentInDollars'),
            func.cast(func.sum(Payment.recipient_count), Integer).label('totalCounts'),
            func.round(func.avg(Payment.base_acres), 2).label('averageAreaInAcres'),
            func.cast(func.sum(Payment.recipient_count) / total_years, BigInteger).label('averageRecipientCount'),
            (func.cast(func.sum(Payment.payment) / program_subquery_total_payment * 100, Numeric(5, 2))).label(
                'totalPaymentInPercentageNationwide'),
            (func.cast(func.sum(Payment.recipient_count) / program_subquery_recipient_count * 100,
                       Numeric(5, 2))).label(
                'averageRecipientCountInPercentageNationwide')
        ).join(
            Program, Payment.program_id == Program.id
        ).filter(
            Payment.program_id == program_id,
            Payment.year.between(start_year, end_year)
        ).group_by(
            Program.name, Payment.state_code
        ).order_by(
            Payment.state_code, desc('totalPaymentInPercentageNationwide')
        )

        # Extract the column names
        column_names = [item['name'] for item in program_query.statement.column_descriptions]

        # Execute the query
        result = program_query.all()

        for row in result:
            response_dict = dict(zip(column_names, row))
            state = response_dict['state']

            # Cleanup / renaming attributes
            response_dict["totalCountsInPercentageNationwide"] = response_dict[
                "averageRecipientCountInPercentageNationwide"]
            response_dict['subPrograms'] = []
            if response_dict['averageAreaInAcres'] is None:
                response_dict['averageAreaInAcres'] = 0.0
            del response_dict['state']

            if state not in program_response_dict:
                program_response_dict[state] = {"programs": [response_dict]}
            else:
                program_response_dict[state]["programs"].append(response_dict)

    subprogram_response_dict = dict()
    for subprogram_id in subprogram_ids:
        # Construct the subquery
        subprogram_subquery = (session.query(func.sum(Payment.payment))
                               .filter(Payment.sub_program_id == subprogram_id, Payment.year.between(start_year, end_year))
                               .label('totalPaymentInDollars'))

        # Construct the main query
        subprogram_query = (session.query(
            Payment.state_code.label('state'),
            Program.name.label('programName'),
            SubProgram.name.label('subProgramName'),
            func.sum(Payment.payment).label('totalPaymentInDollars'),
            (func.cast(func.sum(Payment.payment) / subprogram_subquery * 100, Numeric(5, 2))).label(
                'totalPaymentInPercentageNationwide'),
            func.round(func.avg(Payment.base_acres), 2).label('averageAreaInAcres'),
            func.cast(func.avg(Payment.recipient_count), BigInteger).label('averageRecipientCount')
        ).join(
            SubProgram, Payment.sub_program_id == SubProgram.id
        ).join(
            Program, Payment.program_id == Program.id
        ).filter(
            Payment.sub_program_id == subprogram_id,
            Payment.year.between(start_year, end_year)
        ).group_by(
            Program.name, SubProgram.name, Payment.state_code
        ).order_by(
            Payment.state_code, desc('totalPaymentInPercentageNationwide')
        ))

        # Execute the query
        result = subprogram_query.all()

        # Extract the column names
        column_names = [item['name'] for item in subprogram_query.statement.column_descriptions]

        for row in result:
            response_dict = dict(zip(column_names, row))
            state = response_dict['state']
            program_name = response_dict['programName']

            # Cleanup / renaming attributes
            if response_dict['averageAreaInAcres'] is None:
                response_dict['averageAreaInAcres'] = 0.0
            del response_dict['state']
            del response_dict['programName']

            if state not in subprogram_response_dict:
                subprogram_response_dict[state] = dict()
                subprogram_response_dict[state][program_name] = [response_dict]
            else:
                if program_name in subprogram_response_dict[state]:
                    subprogram_response_dict[state][program_name].append(response_dict)
                else:
                    subprogram_response_dict[state][program_name] = [response_dict]

    # Merge the subtitle and program response dictionaries
    for state in subtitle_response_dict:
        if state in program_response_dict:
            subtitle_response_dict[state].update(program_response_dict[state])
            for program in subtitle_response_dict[state]["programs"]:
                if state in subprogram_response_dict and program["programName"] in subprogram_response_dict[state]:
                    program["subPrograms"] = subprogram_response_dict[state][program["programName"]]

                if subtitle_response_dict[state]["totalPaymentInDollars"] != 0.0:
                    program["totalPaymentInPercentageWithinState"] = (
                        round(program["totalPaymentInDollars"] / subtitle_response_dict[state]["totalPaymentInDollars"] * 100, 2))
                else:
                    program["totalPaymentInPercentageWithinState"] = 0.0

                if subtitle_response_dict[state]["totalCounts"] != 0:
                    program["totalCountsInPercentageWithinState"] = (
                        round(program["totalCounts"] / subtitle_response_dict[state]["totalCounts"] * 100, 2))
                    # TODO: Temporary fix. The below attribute may need to be calculated based on the average recipient count or removed if not needed.
                    program["averageRecipientCountInPercentageWithinState"] = program["totalCountsInPercentageWithinState"]
                else:
                    program["averageRecipientCountInPercentageWithinState"] = 0.0
                    program["totalCountsInPercentageWithinState"] = 0.0

                for subprogram in program["subPrograms"]:
                    if subtitle_response_dict[state]["totalPaymentInDollars"] != 0.0:
                        subprogram["totalPaymentInPercentageWithinState"] = (
                            round(subprogram["totalPaymentInDollars"] /
                                  subtitle_response_dict[state]["totalPaymentInDollars"] * 100, 2))
                    else:
                        subprogram["totalPaymentInPercentageWithinState"] = 0.0
        else:
            subtitle_response_dict[state].update({"programs": []})

    # Create endpoint response dictionary
    endpoint_response_list = []
    for state in subtitle_response_dict:
        endpoint_response_list.append(subtitle_response_dict[state])
    response = {str(start_year) + "-" + str(end_year): endpoint_response_list}

    return response


def generate_title_i_summary_response(subtitle_id, start_year, end_year):
    session = Session()

    subtitle_recipient_avg_count_subquery = (session.query(func.sum(Payment.recipient_count).label("recipientCount"), Payment.year)
                                             .filter(Payment.subtitle_id == subtitle_id, Payment.year.between(start_year, end_year))
                                             .group_by(Payment.year))
    subtitle_avg_recipient_count = session.query(func.avg(subtitle_recipient_avg_count_subquery.subquery().c.recipientCount))

    # Construct the main query
    subtitle_query = (session.query(
        Subtitle.name.label('subtitleName'),
        func.sum(Payment.payment).label('totalPaymentInDollars'),
        func.cast(func.sum(Payment.recipient_count), Integer).label('totalCounts'),
        func.cast(subtitle_avg_recipient_count, BigInteger).label('averageRecipientCount')
    ).join(
        Subtitle, Payment.subtitle_id == Subtitle.id
    ).filter(
        Payment.subtitle_id == subtitle_id, Payment.year.between(start_year, end_year)
    ).group_by(
        Subtitle.name
    ))

    # Extract the column names
    column_names = [item['name'] for item in subtitle_query.statement.column_descriptions]

    # Execute the query
    subtitle_result = subtitle_query.all()

    # Build subtitle response dictionary
    subtitle_response_dict = dict()
    for row in subtitle_result:
        subtitle_response_dict = dict(zip(column_names, row))
        subtitle_response_dict["programs"] = []

    # Find all programs under the subtitle
    subtitle = Subtitle.query.filter_by(id=subtitle_id).first()
    programs = Program.query.filter_by(subtitle_id=subtitle.id).all()
    program_ids = [program.id for program in programs]

    # Construct the subquery
    subtitle_subquery = (session.query(func.sum(Payment.payment))
                         .filter(Payment.subtitle_id == subtitle_id, Payment.year.between(start_year, end_year)).scalar_subquery())

    # For each program, total payment and total payment percentage during the given years
    for program_id in program_ids:

        # Construct the subquery
        program_subquery = (session.query(func.sum(Payment.payment))
                            .filter(Payment.program_id == program_id,
                                    Payment.year.between(start_year, end_year))
                            .label('totalPaymentInDollars'))

        program_recipient_avg_count_subquery = (
            session.query(func.sum(Payment.recipient_count).label("recipientCount"), Payment.year)
            .filter(Payment.program_id == program_id, Payment.year.between(start_year, end_year))
            .group_by(Payment.year))
        program_avg_recipient_count = session.query(
            func.avg(program_recipient_avg_count_subquery.subquery().c.recipientCount))

        # Construct the main query
        program_query = (session.query(
            Program.name.label('programName'),
            func.sum(Payment.payment).label('totalPaymentInDollars'),
            func.cast(func.sum(Payment.recipient_count), Integer).label('totalCounts'),
            func.cast(program_avg_recipient_count, BigInteger).label('averageRecipientCount'),
            (func.cast(func.sum(Payment.payment) / subtitle_subquery * 100, Numeric(5, 2))).label(
                'totalPaymentInPercentage')
        ).join(
            Program, Payment.program_id == Program.id
        ).filter(
            Payment.program_id == program_id,
            Payment.year.between(start_year, end_year)
        ).group_by(
            Program.name
        ))

        # Extract the column names
        column_names = [item['name'] for item in program_query.statement.column_descriptions]

        # Execute the query
        program_result = program_query.all()

        for row in program_result:
            response_dict = dict(zip(column_names, row))

            # Cleanup / renaming attributes
            response_dict['subPrograms'] = []
            subtitle_response_dict["programs"].append(response_dict)

        # For each program, find the subprograms
        subprograms = SubProgram.query.filter_by(program_id=program_id).all()
        subprogram_ids = [subprogram.id for subprogram in subprograms]

        for subprogram_id in subprogram_ids:
            # Construct the main query
            subprogram_query = (session.query(
                Program.name.label('programName'),
                SubProgram.name.label('subProgramName'),
                func.sum(Payment.payment).label('totalPaymentInDollars'),
                (func.cast(func.sum(Payment.payment) / program_subquery * 100, Numeric(5, 2))).label(
                    'totalPaymentInPercentage')
            ).join(
                SubProgram, Payment.sub_program_id == SubProgram.id
            ).join(
                Program, Payment.program_id == Program.id
            ).filter(
                Payment.sub_program_id == subprogram_id,
                Payment.year.between(start_year, end_year)
            ).group_by(
                Program.name, SubProgram.name
            ))

            # Execute the query
            subprogram_result = subprogram_query.all()

            # Extract the column names
            column_names = [item['name'] for item in subprogram_query.statement.column_descriptions]

            for row in subprogram_result:
                response_dict = dict(zip(column_names, row))
                program_name = response_dict['programName']
                del response_dict['programName']

                for program in subtitle_response_dict["programs"]:
                    if program["programName"] == program_name:
                        program["subPrograms"].append(response_dict)

    return subtitle_response_dict


def generate_title_ii_state_distribution_response(program_id, start_year, end_year, practice_code=None):
    session = Session()

    # Get program name
    program_name = session.query(Program.name).filter(Program.id == program_id).first()[0]

    total_crp_sub_program_id = None
    if program_name == TITLE_II_CRP_PROGRAM_NAME:
        # Find ID of the sub program with name 'Total CRP' for the program
        total_crp_sub_program_id = session.query(SubProgram.id).filter(SubProgram.program_id == program_id,
                                                                       SubProgram.name == 'Total CRP').first()[0]

    # Get sub programs for the program
    sub_programs_query = session.query(SubProgram.id.label('subProgramId'),
                                       SubProgram.name.label("subProgramName")
                                       ).filter(SubProgram.program_id == program_id)

    # Extract the column names
    sub_programs_column_names = [item['name'] for item in sub_programs_query.statement.column_descriptions]

    # Execute the query
    sub_programs_result = sub_programs_query.all()

    sub_programs_dict = dict()
    for row in sub_programs_result:
        response_dict = dict(zip(sub_programs_column_names, row))
        sub_program_name = response_dict['subProgramName']
        del response_dict['subProgramName']

        sub_programs_dict[sub_program_name] = response_dict

    # Get sub-sub programs for the sub program
    for sub_program_name in sub_programs_dict:

        sub_sub_programs_query = session.query(SubSubProgram.id.label('subSubProgramId'),
                                               SubSubProgram.name.label("subSubProgramName")
                                               ).filter(SubSubProgram.sub_program_id == sub_programs_dict[sub_program_name]['subProgramId'])

        # Extract the column names
        sub_sub_programs_column_names = [item['name'] for item in sub_sub_programs_query.statement.column_descriptions]

        # Execute the query
        sub_sub_programs_result = sub_sub_programs_query.all()

        sub_sub_programs_list = []
        for row in sub_sub_programs_result:
            response_dict = dict(zip(sub_sub_programs_column_names, row))
            sub_sub_programs_list.append(response_dict)

        sub_programs_dict[sub_program_name]["subSubPrograms"] = sub_sub_programs_list

    # Get practice categories for the program
    practice_categories_query = session.query(
        PracticeCategory.display_name.label('practiceCategoryName'),
        PracticeCategory.category_grouping.label('statuteName')
    ).filter(
        PracticeCategory.program_id == program_id
    )

    # Extract the column names
    practice_categories_column_names = [item['name'] for item in practice_categories_query.statement.column_descriptions]

    # Execute the query
    practice_categories_result = practice_categories_query.all()

    practice_categories_dict = dict()
    for row in practice_categories_result:
        response_dict = dict(zip(practice_categories_column_names, row))
        statute_name = response_dict['statuteName']

        # Cleanup / renaming attributes
        del response_dict['statuteName']

        response_dict["totalPaymentInDollars"] = 0.0
        response_dict["totalPaymentInPercentageNationwide"] = 0.0
        response_dict["totalPaymentInPercentageWithinState"] = 0.0

        if statute_name not in practice_categories_dict:
            practice_categories_dict[statute_name] = {'practiceCategories': [response_dict]}
        else:
            practice_categories_dict[statute_name]['practiceCategories'].append(response_dict)

    # Extract practice category groupings from the practice categories dict
    practice_category_groupings = list()
    for statute_name in practice_categories_dict:
        practice_category_groupings.append(statute_name)

    # Get total payment for each state based on practice category groupings
    state_total_payment_by_practice_category_grouping_query = (session.query(
        Payment.state_code.label('state'),
        PracticeCategory.category_grouping.label('statuteName'),
        func.sum(Payment.payment).label('totalPaymentInDollars')
    ).join(
        PracticeCategory, Payment.practice_category_id == PracticeCategory.id
    ).filter(
        Payment.program_id == program_id,
        Payment.year.between(start_year, end_year),
        PracticeCategory.program_id == program_id
    ).group_by(
        Payment.state_code, PracticeCategory.category_grouping,
    ).order_by(
        Payment.state_code, PracticeCategory.category_grouping
    ))

    # Extract the column names
    state_total_payment_by_practice_category_grouping_column_names = [item['name'] for item in state_total_payment_by_practice_category_grouping_query.statement.column_descriptions]

    # Execute the query
    state_total_payment_by_practice_category_grouping_result = state_total_payment_by_practice_category_grouping_query.all()

    # Create result dictionary
    state_practice_category_grouping_dict = dict()
    total_payment_by_practice_category_grouping_dict = dict()
    for row in state_total_payment_by_practice_category_grouping_result:
        response_dict = dict(zip(state_total_payment_by_practice_category_grouping_column_names, row))
        state = response_dict['state']

        # Cleanup / renaming attributes
        del response_dict['state']

        if state in state_practice_category_grouping_dict:
            state_practice_category_grouping_dict[state]["statutes"].append(response_dict)
        else:
            state_practice_category_grouping_dict[state] = {"statutes": [response_dict]}

        # Calculate total payment by practice category groupings
        if response_dict['statuteName'] in total_payment_by_practice_category_grouping_dict:
            total_payment_by_practice_category_grouping_dict[response_dict['statuteName']] += response_dict['totalPaymentInDollars']
        else:
            total_payment_by_practice_category_grouping_dict[response_dict['statuteName']] = response_dict['totalPaymentInDollars']

    # Add missing statutes with zero payment
    for state in state_practice_category_grouping_dict:
        practice_category_groupings_copy = practice_category_groupings.copy()

        for statute in state_practice_category_grouping_dict[state]["statutes"]:
            if statute["statuteName"] in practice_category_groupings_copy:
                practice_category_groupings_copy.remove(statute["statuteName"])

        for statute_name in practice_category_groupings_copy:
            state_practice_category_grouping_dict[state]["statutes"].append({
                "statuteName": statute_name,
                "totalPaymentInDollars": 0.0
            })

    # Get total payment by practice categories
    state_total_payment_by_practice_category_query = (session.query(
        Payment.state_code.label('state'),
        PracticeCategory.display_name.label('practiceCategoryName'),
        PracticeCategory.category_grouping.label('statuteName'),
        func.sum(Payment.payment).label('totalPaymentInDollars')
    ).join(
        PracticeCategory, Payment.practice_category_id == PracticeCategory.id
    ).filter(
        Payment.program_id == program_id,
        Payment.year.between(start_year, end_year),
        PracticeCategory.program_id == program_id
    ).group_by(
        Payment.state_code, PracticeCategory.category_grouping, PracticeCategory.display_name
    ).order_by(
        Payment.state_code, PracticeCategory.category_grouping, PracticeCategory.display_name
    ))

    # Extract the column names
    state_total_payment_by_practice_categories_column_names = [item['name'] for item in state_total_payment_by_practice_category_query.statement.column_descriptions]

    # Execute the query
    state_total_payment_by_practice_categories_result = state_total_payment_by_practice_category_query.all()

    # Generate result dictionary
    state_total_payment_by_practice_categories_dict = dict()
    for row in state_total_payment_by_practice_categories_result:
        response_dict = dict(zip(state_total_payment_by_practice_categories_column_names, row))
        state = response_dict['state']
        statute_name = response_dict['statuteName']

        # Cleanup / renaming attributes
        del response_dict['state']
        del response_dict['statuteName']
        response_dict["totalPaymentInPercentageNationwide"] = 0.0
        response_dict["totalPaymentInPercentageWithinState"] = 0.0

        if state in state_total_payment_by_practice_categories_dict:
            if statute_name in state_total_payment_by_practice_categories_dict[state]:
                state_total_payment_by_practice_categories_dict[state][statute_name]['practiceCategories'].append(response_dict)
            else:
                state_total_payment_by_practice_categories_dict[state][statute_name] = {'practiceCategories': [response_dict]}
        else:
            state_total_payment_by_practice_categories_dict[state] = {statute_name: {'practiceCategories': [response_dict]}}

    # add missing practice categories with zero payment
    for state in state_total_payment_by_practice_categories_dict:

        for statute in state_total_payment_by_practice_categories_dict[state]:
            statute_dict = state_total_payment_by_practice_categories_dict[state][statute]
            for practice_category in practice_categories_dict[statute]['practiceCategories']:
                found = False
                for practice in statute_dict['practiceCategories']:
                    if practice['practiceCategoryName'] == practice_category['practiceCategoryName']:
                        found = True
                        break
                if not found:
                    statute_dict['practiceCategories'].append({
                        'practiceCategoryName': practice_category['practiceCategoryName'],
                        'totalPaymentInDollars': 0.0,
                        'totalPaymentInPercentageNationwide': 0.0,
                        'totalPaymentInPercentageWithinState': 0.0
                    })

        for statute_name in practice_categories_dict:
            if statute_name not in state_total_payment_by_practice_categories_dict[state]:
                state_total_payment_by_practice_categories_dict[state].update({statute_name: practice_categories_dict[statute_name]})

    for state in state_total_payment_by_practice_categories_dict:
        for statute in state_total_payment_by_practice_categories_dict[state]:
            state_total_payment_by_practice_categories_dict[state][statute]['practiceCategories'] = sorted(state_total_payment_by_practice_categories_dict[state][statute]['practiceCategories'], key=lambda x: x['totalPaymentInDollars'], reverse=True)

    # Get practice codes list, if provided in the request
    practice_codes_list = practice_code.split("|") if practice_code else []

    # Get total payment by practice codes
    state_total_payment_by_practice_code_query = (session.query(
        Payment.state_code.label('state'),
        PracticeCategory.display_name.label('practiceCategoryName'),
        Payment.practice_code.label('practiceCode'),
        Practice.name.label('practiceName'),
        func.sum(Payment.payment).label('totalPaymentInDollars')
    ).join(
        PracticeCategory, Payment.practice_category_id == PracticeCategory.id
    ).join(
        Practice, Payment.practice_code == Practice.code
    ).filter(
        Payment.program_id == program_id,
        Payment.year.between(start_year, end_year),
        PracticeCategory.program_id == program_id,
        Payment.practice_code.in_(practice_codes_list) if practice_codes_list else True
    ).group_by(
        Payment.state_code, PracticeCategory.display_name,
        Payment.practice_code, Practice.name
    ).order_by(
        Payment.state_code, PracticeCategory.display_name, Payment.practice_code
    ))

    # Extract the column names
    state_total_payment_by_practice_code_column_names = [item['name'] for item in state_total_payment_by_practice_code_query.statement.column_descriptions]

    # Execute the query
    state_total_payment_by_practice_code_result = state_total_payment_by_practice_code_query.all()

    # Generate result dictionary
    state_total_payment_by_practice_code_dict = dict()

    for row in state_total_payment_by_practice_code_result:
        response_dict = dict(zip(state_total_payment_by_practice_code_column_names, row))

        state = response_dict['state']
        practice_category_name = response_dict['practiceCategoryName']
        response_dict['practiceName'] = str(response_dict['practiceName']) + ' (' + response_dict['practiceCode'] + ')'

        # Cleanup / renaming attributes
        del response_dict['state']
        del response_dict['practiceCode']
        del response_dict['practiceCategoryName']

        if state in state_total_payment_by_practice_code_dict:
            if practice_category_name in state_total_payment_by_practice_code_dict[state]:
                state_total_payment_by_practice_code_dict[state][practice_category_name]['practices'].append(response_dict)
            else:
                state_total_payment_by_practice_code_dict[state][practice_category_name] = {'practices': [response_dict]}
        else:
            state_total_payment_by_practice_code_dict[state] = {practice_category_name: {'practices': [response_dict]}}

    for state in state_total_payment_by_practice_categories_dict:
        for statute in state_total_payment_by_practice_categories_dict[state]:
            for practice_category in state_total_payment_by_practice_categories_dict[state][statute]['practiceCategories']:
                if state in state_total_payment_by_practice_code_dict and practice_category['practiceCategoryName'] in state_total_payment_by_practice_code_dict[state]:
                    practice_category['practices'] = state_total_payment_by_practice_code_dict[state][practice_category['practiceCategoryName']]['practices']
                else:
                    practice_category['practices'] = []

    # Get sum of payment for the given period grouped by practice category
    total_payment_by_practice_categories_query = (session.query(
        PracticeCategory.display_name.label('practiceCategoryName'),
        func.sum(Payment.payment).label('totalPaymentInDollars')
    ).join(
        PracticeCategory, Payment.practice_category_id == PracticeCategory.id
    ).filter(
        Payment.program_id == program_id,
        Payment.year.between(start_year, end_year),
        PracticeCategory.program_id == program_id
    ).group_by(
        PracticeCategory.display_name
    ).order_by(
        desc('totalPaymentInDollars')
    ))

    # Extract the column names
    total_payment_by_practice_categories_column_names = [item['name'] for item in
                                                         total_payment_by_practice_categories_query.statement.column_descriptions]

    # Execute the query
    total_payment_by_practice_categories_result = total_payment_by_practice_categories_query.all()

    # Generate result dictionary
    total_payment_by_practice_categories_dict = dict()
    for row in total_payment_by_practice_categories_result:
        response_dict = dict(zip(total_payment_by_practice_categories_column_names, row))
        practice_category_name = response_dict['practiceCategoryName']

        # Cleanup / renaming attributes
        del response_dict['practiceCategoryName']

        total_payment_by_practice_categories_dict[practice_category_name] = response_dict

    # Get total values for by sub programs by state
    state_total_values_by_sub_programs_query = (session.query(
        Payment.state_code.label('state'),
        SubProgram.name.label('subProgramName'),
        func.sum(Payment.payment).label('totalPaymentInDollars'),
        func.cast(func.sum(Payment.recipient_count).label('totalRecipients'), Integer),
        func.cast(func.sum(Payment.farm_count).label('totalFarms'), Integer),
        func.cast(func.sum(Payment.contract_count).label('totalContracts'), Integer),
        func.cast(func.sum(Payment.base_acres).label('totalAreaInAcres'), Integer),
    ).join(
        SubProgram, Payment.sub_program_id == SubProgram.id
    ).filter(
        Payment.program_id == program_id,
        Payment.year.between(start_year, end_year),
        Payment.sub_sub_program_id == None  # noqa: Needed for SQLAlchemy
    ).group_by(
        Payment.state_code, SubProgram.name
    ).order_by(
        desc('totalPaymentInDollars')
    ))

    # Extract the column names
    state_total_values_by_sub_programs_column_names = [item['name'] for item in state_total_values_by_sub_programs_query.statement.column_descriptions]

    # Execute the query
    state_total_values_by_sub_programs_result = state_total_values_by_sub_programs_query.all()

    # Generate result dictionary
    state_total_values_by_sub_programs_dict = dict()

    for row in state_total_values_by_sub_programs_result:
        response_dict = dict(zip(state_total_values_by_sub_programs_column_names, row))
        state = response_dict['state']

        # Cleanup / renaming attributes
        del response_dict['state']
        response_dict["totalPaymentInPercentageNationwide"] = 0.0
        response_dict["totalPaymentInPercentageWithinState"] = 0.0
        response_dict["totalRecipientsInPercentageWithinState"] = 0.0
        response_dict["totalRecipientsInPercentageNationwide"] = 0.0
        response_dict["totalFarmsInPercentageWithinState"] = 0.0
        response_dict["totalFarmsInPercentageNationwide"] = 0.0
        response_dict["totalContractsInPercentageWithinState"] = 0.0
        response_dict["totalContractsInPercentageNationwide"] = 0.0
        response_dict["totalAreaInPercentageWithinState"] = 0.0
        response_dict["totalAreaInPercentageNationwide"] = 0.0
        response_dict["subSubPrograms"] = []

        # In CRP, exclude 'Total CRP' sub program from the response
        if program_name == TITLE_II_CRP_PROGRAM_NAME and response_dict['subProgramName'] != 'Total CRP':
            if state in state_total_values_by_sub_programs_dict:
                state_total_values_by_sub_programs_dict[state]["subPrograms"].append(response_dict)
            else:
                state_total_values_by_sub_programs_dict[state] = {"subPrograms": [response_dict]}

    # Get total values by sub programs
    total_values_by_sub_programs_query = (session.query(
        SubProgram.name.label('subProgramName'),
        func.sum(Payment.payment).label('totalPaymentInDollars'),
        func.cast(func.sum(Payment.recipient_count).label('totalRecipients'), Integer),
        func.cast(func.sum(Payment.farm_count).label('totalFarms'), Integer),
        func.cast(func.sum(Payment.contract_count).label('totalContracts'), Integer),
        func.cast(func.sum(Payment.base_acres).label('totalAreaInAcres'), Integer),
    ).join(
        SubProgram, Payment.sub_program_id == SubProgram.id
    ).filter(
        Payment.program_id == program_id,
        Payment.year.between(start_year, end_year),
        Payment.sub_sub_program_id == None  # noqa: Needed for SQLAlchemy
    ).group_by(
        SubProgram.name
    ).order_by(
        desc('totalPaymentInDollars')
    ))

    # Extract the column names
    total_values_by_sub_programs_column_names = [item['name'] for item in total_values_by_sub_programs_query.statement.column_descriptions]

    # Execute the query
    total_values_by_sub_programs_result = total_values_by_sub_programs_query.all()

    # Generate result dictionary
    total_values_by_sub_programs_dict = dict()

    for row in total_values_by_sub_programs_result:
        response_dict = dict(zip(total_values_by_sub_programs_column_names, row))
        sub_program_name = response_dict['subProgramName']

        # Cleanup / renaming attributes
        del response_dict['subProgramName']

        total_values_by_sub_programs_dict[sub_program_name] = response_dict

    # Get total values by sub-sub programs by state
    state_total_values_by_sub_sub_programs_query = (session.query(
        Payment.state_code.label('state'),
        SubSubProgram.name.label('subSubProgramName'),
        func.sum(Payment.payment).label('totalPaymentInDollars'),
        func.cast(func.sum(Payment.recipient_count).label('totalRecipients'), Integer),
        func.cast(func.sum(Payment.farm_count).label('totalFarms'), Integer),
        func.cast(func.sum(Payment.contract_count).label('totalContracts'), Integer),
        func.cast(func.sum(Payment.base_acres).label('totalAreaInAcres'), Integer),
    ).join(
        SubSubProgram, Payment.sub_sub_program_id == SubSubProgram.id
    ).filter(
        Payment.program_id == program_id,
        Payment.year.between(start_year, end_year)
    ).group_by(
        Payment.state_code, SubSubProgram.name
    ).order_by(
        desc('totalPaymentInDollars')
    ))

    # Extract the column names
    state_total_values_by_sub_sub_programs_column_names = [item['name'] for item in state_total_values_by_sub_sub_programs_query.statement.column_descriptions]

    # Execute the query
    state_total_values_by_sub_sub_programs_result = state_total_values_by_sub_sub_programs_query.all()

    # Generate result dictionary
    state_total_values_by_sub_sub_programs_dict = dict()

    for row in state_total_values_by_sub_sub_programs_result:
        response_dict = dict(zip(state_total_values_by_sub_sub_programs_column_names, row))
        state = response_dict['state']
        sub_sub_program_name = response_dict['subSubProgramName']

        # Cleanup / renaming attributes
        del response_dict['state']
        # del response_dict['subSubProgramName']

        response_dict["totalPaymentInPercentageNationwide"] = 0.0
        response_dict["totalPaymentInPercentageWithinState"] = 0.0
        response_dict["totalRecipientsInPercentageWithinState"] = 0.0
        response_dict["totalRecipientsInPercentageNationwide"] = 0.0
        response_dict["totalFarmsInPercentageWithinState"] = 0.0
        response_dict["totalFarmsInPercentageNationwide"] = 0.0
        response_dict["totalContractsInPercentageWithinState"] = 0.0
        response_dict["totalContractsInPercentageNationwide"] = 0.0
        response_dict["totalAreaInPercentageWithinState"] = 0.0
        response_dict["totalAreaInPercentageNationwide"] = 0.0

        if state in state_total_values_by_sub_sub_programs_dict:
            state_total_values_by_sub_sub_programs_dict[state].append({sub_sub_program_name: response_dict})
        else:
            state_total_values_by_sub_sub_programs_dict[state] = [{sub_sub_program_name: response_dict}]

    # Sort the sub-sub programs by alphabetical order of their names
    for state in state_total_values_by_sub_sub_programs_dict:
        state_total_values_by_sub_sub_programs_dict[state] = sorted(state_total_values_by_sub_sub_programs_dict[state], key=lambda x: list(x.keys())[0])

    # Get total values by sub-sub programs
    total_values_by_sub_sub_programs_query = (session.query(
        SubSubProgram.name.label('subSubProgramName'),
        func.sum(Payment.payment).label('totalPaymentInDollars'),
        func.cast(func.sum(Payment.recipient_count).label('totalRecipients'), Integer),
        func.cast(func.sum(Payment.farm_count).label('totalFarms'), Integer),
        func.cast(func.sum(Payment.contract_count).label('totalContracts'), Integer),
        func.cast(func.sum(Payment.base_acres).label('totalAreaInAcres'), Integer),
    ).join(
        SubSubProgram, Payment.sub_sub_program_id == SubSubProgram.id
    ).filter(
        Payment.program_id == program_id,
        Payment.year.between(start_year, end_year)
    ).group_by(
        SubSubProgram.name
    ).order_by(
        desc('totalPaymentInDollars')
    ))

    # Extract the column names
    total_values_by_sub_sub_programs_column_names = [item['name'] for item in total_values_by_sub_sub_programs_query.statement.column_descriptions]

    # Execute the query
    total_values_by_sub_sub_programs_result = total_values_by_sub_sub_programs_query.all()

    # Generate result dictionary
    total_values_by_sub_sub_programs_dict = dict()

    for row in total_values_by_sub_sub_programs_result:
        response_dict = dict(zip(total_values_by_sub_sub_programs_column_names, row))
        sub_sub_program_name = response_dict['subSubProgramName']

        # Cleanup / renaming attributes
        del response_dict['subSubProgramName']

        total_values_by_sub_sub_programs_dict[sub_sub_program_name] = response_dict

    # Total payment for the given period. Special handling for CRP, as its 'Total CRP' sub program contains the total values.
    if program_name != TITLE_II_CRP_PROGRAM_NAME:
        total_payments_subquery = session.query(func.sum(Payment.payment).label('totalPaymentInDollars')).filter(
            Payment.program_id == program_id,
            Payment.year.between(start_year, end_year),
            Payment.sub_sub_program_id == None  # noqa: Needed for SQLAlchemy
        )
    else:
        total_payments_subquery = session.query(func.sum(Payment.payment).label('totalPaymentInDollars')).filter(
            Payment.program_id == program_id,
            Payment.sub_program_id == total_crp_sub_program_id,
            Payment.year.between(start_year, end_year),
            Payment.sub_sub_program_id == None  # noqa: Needed for SQLAlchemy
        )
    nationwide_total_payment = total_payments_subquery.scalar()

    # Total recipients for the given period
    if program_name != TITLE_II_CRP_PROGRAM_NAME:
        total_recipients_subquery = session.query(func.sum(Payment.recipient_count).label('totalRecipients')).filter(
            Payment.program_id == program_id,
            Payment.year.between(start_year, end_year),
            Payment.sub_sub_program_id == None  # noqa: Needed for SQLAlchemy
        )
    else:
        total_recipients_subquery = session.query(func.sum(Payment.recipient_count).label('totalRecipients')).filter(
            Payment.program_id == program_id,
            Payment.sub_program_id == total_crp_sub_program_id,
            Payment.year.between(start_year, end_year),
            Payment.sub_sub_program_id == None  # noqa: Needed for SQLAlchemy
        )
    nationwide_total_recipients = total_recipients_subquery.scalar()

    # Total contracts for the given period
    if program_name != TITLE_II_CRP_PROGRAM_NAME:
        total_contracts_subquery = session.query(func.sum(Payment.contract_count).label('totalContracts')).filter(
            Payment.program_id == program_id,
            Payment.year.between(start_year, end_year),
            Payment.sub_sub_program_id == None  # noqa: Needed for SQLAlchemy
        )
    else:
        total_contracts_subquery = session.query(func.sum(Payment.contract_count).label('totalContracts')).filter(
            Payment.program_id == program_id,
            Payment.sub_program_id == total_crp_sub_program_id,
            Payment.year.between(start_year, end_year),
            Payment.sub_sub_program_id == None  # noqa: Needed for SQLAlchemy
        )
    nationwide_total_contracts = total_contracts_subquery.scalar()

    # Total farms for the given period
    if program_name != TITLE_II_CRP_PROGRAM_NAME:
        total_farms_subquery = session.query(func.sum(Payment.farm_count).label('totalFarms')).filter(
            Payment.program_id == program_id,
            Payment.year.between(start_year, end_year),
            Payment.sub_sub_program_id == None  # noqa: Needed for SQLAlchemy
        )
    else:
        total_farms_subquery = session.query(func.sum(Payment.farm_count).label('totalFarms')).filter(
            Payment.program_id == program_id,
            Payment.sub_program_id == total_crp_sub_program_id,
            Payment.year.between(start_year, end_year),
            Payment.sub_sub_program_id == None  # noqa: Needed for SQLAlchemy
        )
    nationwide_total_farms = total_farms_subquery.scalar()

    # Total area in acres for the given period
    if program_name != TITLE_II_CRP_PROGRAM_NAME:
        total_area_in_acres_subquery = session.query(func.sum(Payment.base_acres).label('totalAreaInAcres')).filter(
            Payment.program_id == program_id,
            Payment.year.between(start_year, end_year),
            Payment.sub_sub_program_id == None  # noqa: Needed for SQLAlchemy
        )
    else:
        total_area_in_acres_subquery = session.query(func.sum(Payment.base_acres).label('totalAreaInAcres')).filter(
            Payment.program_id == program_id,
            Payment.sub_program_id == total_crp_sub_program_id,
            Payment.year.between(start_year, end_year),
            Payment.sub_sub_program_id == None  # noqa: Needed for SQLAlchemy
        )
    nationwide_total_area_in_acres = total_area_in_acres_subquery.scalar()

    # Top-level query
    query = session.query(
        Payment.state_code.label('state'),
        func.sum(Payment.payment).label('totalPaymentInDollars'),
        func.cast(func.sum(Payment.recipient_count).label('totalRecipients'), Integer),
        func.cast(func.sum(Payment.farm_count).label('totalFarms'), Integer),
        func.cast(func.sum(Payment.contract_count).label('totalContracts'), Integer),
        func.cast(func.sum(Payment.base_acres).label('totalAreaInAcres'), Integer),
        (func.cast(func.sum(Payment.payment) / nationwide_total_payment * 100, Numeric(5, 2))).label('totalPaymentInPercentageNationwide'),
        (func.cast(func.sum(Payment.recipient_count) / nationwide_total_recipients * 100, Numeric(5, 2))).label('totalRecipientsInPercentageNationwide'),
        (func.cast(func.sum(Payment.farm_count) / nationwide_total_farms * 100, Numeric(5, 2))).label('totalFarmsInPercentageNationwide'),
        (func.cast(func.sum(Payment.contract_count) / nationwide_total_contracts * 100, Numeric(5, 2))).label('totalContractsInPercentageNationwide'),
        (func.cast(func.sum(Payment.base_acres) / nationwide_total_area_in_acres * 100, Numeric(5, 2))).label('totalAreaInPercentageNationwide')
    ).filter(
        Payment.program_id == program_id,
        Payment.year.between(start_year, end_year),
        Payment.sub_sub_program_id == None  # noqa: Needed for SQLAlchemy
    ).group_by(
        Payment.state_code
    ).order_by(
        desc('totalPaymentInDollars')
    )

    if program_name != TITLE_II_CRP_PROGRAM_NAME:
        query = query.filter(
            Payment.program_id == program_id,
            Payment.year.between(start_year, end_year),
            Payment.sub_sub_program_id == None  # noqa: Needed for SQLAlchemy
        )
    # In CRP, use the 'Total CRP' sub program to calculate the top-level total values
    else:
        query = query.filter(
            Payment.program_id == program_id,
            Payment.sub_program_id == total_crp_sub_program_id,
            Payment.year.between(start_year, end_year),
            Payment.sub_sub_program_id == None  # noqa: Needed for SQLAlchemy
        )

    # Extract the column names
    column_names = [item['name'] for item in query.statement.column_descriptions]

    # Execute the query
    result = query.all()

    # Generate result dictionary
    program_response_dict = dict()
    for row in result:
        response_dict = dict(zip(column_names, row))
        state = response_dict['state']
        program_response_dict[state] = response_dict

    # Complete the program response dictionary
    for state in program_response_dict:
        state_dict = program_response_dict[state]

        if state in state_practice_category_grouping_dict:
            state_dict.update(state_practice_category_grouping_dict[state])
        if "statutes" in state_dict:
            for statute in state_dict['statutes']:
                # skip statutes that have no totals entry yet
                if statute['statuteName'] not in total_payment_by_practice_category_grouping_dict:
                    continue

                for practice_category in state_total_payment_by_practice_categories_dict[state][statute['statuteName']]['practiceCategories']:
                    practice_category_name = practice_category['practiceCategoryName']

                    if practice_category_name in total_payment_by_practice_categories_dict:
                        practice_category['totalPaymentInPercentageNationwide'] = round(practice_category['totalPaymentInDollars'] / total_payment_by_practice_categories_dict[practice_category["practiceCategoryName"]]['totalPaymentInDollars'] * 100, 2)
                    practice_category['totalPaymentInPercentageWithinState'] = round(practice_category['totalPaymentInDollars'] / state_dict['totalPaymentInDollars'] * 100, 2)

                statute.update(state_total_payment_by_practice_categories_dict[state][statute['statuteName']])
                statute['totalPaymentInPercentageWithinState'] = round(statute['totalPaymentInDollars'] / state_dict['totalPaymentInDollars'] * 100, 2)
                statute['totalPaymentInPercentageNationwide'] = round(statute['totalPaymentInDollars'] / total_payment_by_practice_category_grouping_dict[statute['statuteName']] * 100, 2)

        if state in state_total_values_by_sub_programs_dict:
            state_dict.update(state_total_values_by_sub_programs_dict[state])

            for sub_program in state_dict["subPrograms"]:
                sub_program_name = sub_program["subProgramName"]
                if sub_program_name in total_values_by_sub_programs_dict:
                    __calculate_and_add_percentages(state_dict, sub_program, total_values_by_sub_programs_dict, sub_program_name)

                if sub_program_name in sub_programs_dict and "subSubPrograms" in sub_programs_dict[sub_program_name] and len(sub_programs_dict[sub_program_name]["subSubPrograms"]) > 0 and state in state_total_values_by_sub_sub_programs_dict:
                    for sub_sub_program_dict in state_total_values_by_sub_sub_programs_dict[state]:
                        for sub_sub_program_temp in sub_programs_dict[sub_program_name]["subSubPrograms"]:
                            sub_sub_program_name = list(sub_sub_program_dict.keys())[0]
                            sub_sub_program = sub_sub_program_dict[sub_sub_program_name]
                            if sub_sub_program_name == sub_sub_program_temp["subSubProgramName"]:
                                __calculate_and_add_percentages(state_dict, sub_sub_program, total_values_by_sub_sub_programs_dict, sub_sub_program_name)
                                sub_program["subSubPrograms"].append(sub_sub_program)
    # Create endpoint response dictionary
    endpoint_response_list = []
    for state in program_response_dict:
        endpoint_response_list.append(program_response_dict[state])
    response = {str(start_year) + "-" + str(end_year): endpoint_response_list}

    return response


def generate_title_xi_state_distribution_response(program_id, start_year, end_year):
    session = Session()

    num_years = end_year - start_year + 1

    # construct the query
    program_query = session.query(
        Payment.state_code.label('state'),
        Program.name.label('programName'),
        Payment.year.label('year'),
        Payment.base_acres.label('base_acres'),
        Payment.premium_policy_count.label('premium_policy_count'),
        Payment.liability_amount.label('liability_amount'),
        Payment.premium_amount.label('premium_amount'),
        Payment.premium_subsidy_amount.label('premium_subsidy_amount'),
        Payment.indemnity_amount.label('indemnity_amount'),
        Payment.farmer_premium_amount.label('farmer_premium_amount'),
        Payment.loss_ratio.label('loss_ratio'),
        Payment.net_farmer_benefit_amount.label('net_farmer_benefit_amount')).join(
        Program, Payment.program_id == Program.id).filter(
        Payment.program_id == program_id,
        Payment.year.between(start_year, end_year)
    )

    # execute the query
    program_result = program_query.all()

    # create dictionaries
    program_response_dict = defaultdict(list)
    year_dict = defaultdict(list)

    # aggregate data
    for record in program_result:
        year = str(record[2])
        state = record[0]
        base_acres = record[3]
        premium_policy_count = record[4]
        liability_amount = record[5]
        premium_amount = record[6]
        premium_subsidy_amount = record[7]
        indemnity_amount = record[8]
        farmer_premium_amount = record[9]
        loss_ratio = record[10]
        net_farmer_benefit_amount = record[11]

        year_dict[year].append({
            'state': state,
            'totalIndemnitiesInDollars': indemnity_amount,
            'totalPremiumInDollars': premium_amount,
            'totalPremiumSubsidyInDollars': premium_subsidy_amount,
            'totalFarmerPaidPremiumInDollars': farmer_premium_amount,
            'totalNetFarmerBenefitInDollars': net_farmer_benefit_amount,
            'totalPoliciesEarningPremium': premium_policy_count,
            'totalLiabilitiesInDollars': liability_amount,
            'totalInsuredAreaInAcres': base_acres,
            'lossRatio': loss_ratio
        })

    state_aggregate_dict = defaultdict(lambda: {
        'state': '',
        'totalIndemnitiesInDollars': 0,
        'totalPremiumInDollars': 0,
        'totalPremiumSubsidyInDollars': 0,
        'totalFarmerPaidPremiumInDollars': 0,
        'totalNetFarmerBenefitInDollars': 0,
        'totalPoliciesEarningPremium': 0,
        'totalLiabilitiesInDollars': 0,
        'totalInsuredAreaInAcres': 0,
        'averageLiabilitiesInDollars': 0,
        'averageInsuredAreaInAcres': 0,
        'lossRatio': 0,
        'subPrograms': []
    })

    # Loop through each year and aggregate data by state
    for year, records in year_dict.items():
        for record in records:
            state = record['state']

            # Sum the values across all years for each state
            state_aggregate_dict[state]['totalIndemnitiesInDollars'] += record['totalIndemnitiesInDollars']
            state_aggregate_dict[state]['totalPremiumInDollars'] += record['totalPremiumInDollars']
            state_aggregate_dict[state]['totalPremiumSubsidyInDollars'] += record['totalPremiumSubsidyInDollars']
            state_aggregate_dict[state]['totalFarmerPaidPremiumInDollars'] += record['totalFarmerPaidPremiumInDollars']
            state_aggregate_dict[state]['totalNetFarmerBenefitInDollars'] += record['totalNetFarmerBenefitInDollars']
            state_aggregate_dict[state]['totalPoliciesEarningPremium'] += record['totalPoliciesEarningPremium']
            state_aggregate_dict[state]['totalLiabilitiesInDollars'] += record['totalLiabilitiesInDollars']
            state_aggregate_dict[state]['totalInsuredAreaInAcres'] += record['totalInsuredAreaInAcres']

    # Calculate average loss ratio for each state
    for state, values in state_aggregate_dict.items():
        # Calculate average insured area in acres
        values['averageInsuredAreaInAcres'] = values['totalInsuredAreaInAcres'] / num_years
        del values['totalInsuredAreaInAcres']

        # Calculate average liabilities in dollars
        values['averageLiabilitiesInDollars'] = values['totalLiabilitiesInDollars'] / num_years
        del values['totalLiabilitiesInDollars']

        # Loss_ratio is indemnities / premium so create the average loss ratio
        values['lossRatio'] = values['totalIndemnitiesInDollars'] / values['totalPremiumInDollars']

        # round the loss ratio to 3 decimal places
        values['lossRatio'] = round(values['lossRatio'], 3)

    # # sort states by decreasing order of total payment in dollars
    # state_aggregate_dict = dict(state_aggregate_dict)
    # state_aggregate_dict = sorted(state_aggregate_dict.items(), key=lambda x: x[1]['totalIndemnitiesInDollars'],
    #                               reverse=True)

    # modify the structure of the output so the state goes inside the dictionary
    state_aggregate_dict = dict(state_aggregate_dict)

    # convert the data into the required format
    final_output = []
    for state, values in state_aggregate_dict.items():
        values['state'] = state  # add the state into the dictionary
        final_output.append(values)

    # Sort the final output based on totalIndemnitiesInDollars in reverse order
    final_output = sorted(final_output, key=lambda x: x['totalIndemnitiesInDollars'], reverse=True)

    # Add the total states data to the program_response_dict under the key 'TotalStates'
    program_response_dict[str(start_year) + '-' + str(end_year)] = final_output

    return program_response_dict

    # Add the total states data to the program_response_dict under the key 'TotalStates'
    program_response_dict[str(start_year) + '-' + str(end_year)] = state_aggregate_dict

    return program_response_dict


def __calculate_and_add_percentages(state_dict, entity_dict, total_values_dict, entity_name):
    if state_dict["totalPaymentInDollars"] is not None and state_dict["totalPaymentInDollars"] != 0:
        entity_dict["totalPaymentInPercentageWithinState"] = round(
            entity_dict["totalPaymentInDollars"] / state_dict["totalPaymentInDollars"] * 100, 2)
    if state_dict["totalRecipients"] is not None and state_dict["totalRecipients"] != 0:
        entity_dict["totalRecipientsInPercentageWithinState"] = round(
            entity_dict["totalRecipients"] / state_dict["totalRecipients"] * 100, 2)
    if state_dict["totalFarms"] is not None and state_dict["totalFarms"] != 0:
        entity_dict["totalFarmsInPercentageWithinState"] = round(
            entity_dict["totalFarms"] / state_dict["totalFarms"] * 100, 2)
    if state_dict["totalContracts"] is not None and state_dict["totalContracts"] != 0:
        entity_dict["totalContractsInPercentageWithinState"] = round(
            entity_dict["totalContracts"] / state_dict["totalContracts"] * 100, 2)
    if state_dict["totalAreaInAcres"] is not None and state_dict["totalAreaInAcres"] != 0:
        entity_dict["totalAreaInPercentageWithinState"] = round(
            entity_dict["totalAreaInAcres"] / state_dict["totalAreaInAcres"] * 100, 2)
    if total_values_dict[entity_name]["totalPaymentInDollars"] is not None and \
            total_values_dict[entity_name]["totalPaymentInDollars"] != 0:
        entity_dict["totalPaymentInPercentageNationwide"] = round(
            entity_dict["totalPaymentInDollars"] / total_values_dict[entity_name][
                "totalPaymentInDollars"] * 100, 2)
    if total_values_dict[entity_name]["totalRecipients"] is not None and \
            total_values_dict[entity_name]["totalRecipients"] != 0:
        entity_dict["totalRecipientsInPercentageNationwide"] = round(
            entity_dict["totalRecipients"] / total_values_dict[entity_name][
                "totalRecipients"] * 100, 2)
    if total_values_dict[entity_name]["totalFarms"] is not None and \
            total_values_dict[entity_name]["totalFarms"] != 0:
        entity_dict["totalFarmsInPercentageNationwide"] = round(
            entity_dict["totalFarms"] / total_values_dict[entity_name]["totalFarms"] * 100, 2)
    if total_values_dict[entity_name]["totalContracts"] is not None and \
            total_values_dict[entity_name]["totalContracts"] != 0:
        entity_dict["totalContractsInPercentageNationwide"] = round(
            entity_dict["totalContracts"] / total_values_dict[entity_name]["totalContracts"] * 100,
            2)
    if total_values_dict[entity_name]["totalAreaInAcres"] is not None and \
            total_values_dict[entity_name]["totalAreaInAcres"] != 0:
        entity_dict["totalAreaInPercentageNationwide"] = round(
            entity_dict["totalAreaInAcres"] / total_values_dict[entity_name][
                "totalAreaInAcres"] * 100, 2)


def generate_title_ii_summary_response(program_id, start_year, end_year):
    session = Session()

    # Get program name
    program_name = session.query(Program.name).filter(Program.id == program_id).first()[0]

    total_crp_sub_program_id = None
    if program_name == TITLE_II_CRP_PROGRAM_NAME:
        # Find ID of the sub program with name 'Total CRP' for the program
        total_crp_sub_program_id = session.query(SubProgram.id).filter(SubProgram.program_id == program_id,
                                                                       SubProgram.name == 'Total CRP').first()[0]

    # Calculate total values for the given period
    total_values_query = (session.query(func.sum(Payment.payment).label('totalPaymentInDollars'),
                                        func.cast(func.sum(Payment.recipient_count).label('totalRecipients'), Integer),
                                        func.cast(func.sum(Payment.farm_count).label('totalFarms'), Integer),
                                        func.cast(func.sum(Payment.contract_count).label('totalContracts'), Integer),
                                        func.cast(func.sum(Payment.base_acres).label('totalAreaInAcres'), Integer)))

    if program_name != TITLE_II_CRP_PROGRAM_NAME:
        total_values_query = total_values_query.filter(
            Payment.program_id == program_id,
            Payment.year.between(start_year, end_year),
            Payment.sub_sub_program_id == None  # noqa: Needed for SQLAlchemy
        )
    # In CRP, use the 'Total CRP' sub program to calculate the top-level total values
    else:
        total_values_query = total_values_query.filter(
            Payment.program_id == program_id,
            Payment.sub_program_id == total_crp_sub_program_id,
            Payment.year.between(start_year, end_year),
            Payment.sub_sub_program_id == None  # noqa: Needed for SQLAlchemy
        )

    # Extract the column names
    total_values_column_names = [item['name'] for item in total_values_query.statement.column_descriptions]

    # Execute the query
    total_values_result = total_values_query.all()

    # Generate result dictionary
    total_values_dict = dict()

    for row in total_values_result:
        response_dict = dict(zip(total_values_column_names, row))
        total_values_dict = response_dict

    # Get sub programs for the program
    sub_programs_query = session.query(
        SubProgram.name.label('subProgramName'),
        SubProgram.id.label('subProgramId')
    ).filter(SubProgram.program_id == program_id)

    # Extract the column names
    sub_programs_column_names = [item['name'] for item in sub_programs_query.statement.column_descriptions]

    # Execute the query
    sub_programs_result = sub_programs_query.all()

    sub_programs_dict = dict()

    for row in sub_programs_result:
        response_dict = dict(zip(sub_programs_column_names, row))

        # In CRP, exclude 'Total CRP' sub program from the response
        if program_name == TITLE_II_CRP_PROGRAM_NAME and response_dict['subProgramName'] != 'Total CRP':
            response_dict["totalPaymentInDollars"] = 0.0
            response_dict["totalPaymentInPercentage"] = 0.0
            sub_program_name = response_dict['subProgramName']
            sub_programs_dict[sub_program_name] = response_dict

    # Construct the program total subquery
    program_subquery_total_payment = (session.query(func.sum(Payment.payment))
                                      .filter(Payment.program_id == program_id,
                                              Payment.year.between(start_year, end_year))
                                      .label('totalPaymentInDollars'))

    # Get total values by sub programs
    total_values_by_sub_programs_query = (session.query(
        SubProgram.name.label('subProgramName'),
        func.sum(Payment.payment).label('totalPaymentInDollars'),
        func.cast(func.sum(Payment.recipient_count).label('totalRecipients'), Integer),
        func.cast(func.sum(Payment.farm_count).label('totalFarms'), Integer),
        func.cast(func.sum(Payment.contract_count).label('totalContracts'), Integer),
        func.cast(func.sum(Payment.base_acres).label('totalAreaInAcres'), Integer),
        (func.cast(func.sum(Payment.payment) / program_subquery_total_payment * 100, Numeric(5, 2))).label(
            'totalPaymentInPercentage'),

    ).join(
        SubProgram, Payment.sub_program_id == SubProgram.id
    ).filter(
        Payment.program_id == program_id,
        Payment.year.between(start_year, end_year),
        Payment.sub_sub_program_id == None  # noqa: Needed for SQLAlchemy
    ).group_by(
        SubProgram.name
    ))

    # Extract the column names
    total_values_by_sub_programs_column_names = [item['name'] for item in total_values_by_sub_programs_query.statement.column_descriptions]

    # Execute the query
    total_values_by_sub_programs_result = total_values_by_sub_programs_query.all()

    # Generate result dictionary
    total_values_by_sub_programs_dict = dict()

    for row in total_values_by_sub_programs_result:
        response_dict = dict(zip(total_values_by_sub_programs_column_names, row))
        sub_program_name = response_dict['subProgramName']

        # In CRP, exclude 'Total CRP' sub program from the response
        if program_name == TITLE_II_CRP_PROGRAM_NAME and response_dict['subProgramName'] != 'Total CRP':
            # Cleanup / renaming attributes
            del response_dict['subProgramName']
            total_values_by_sub_programs_dict[sub_program_name] = response_dict

    for sub_program_name in sub_programs_dict:
        # Get sub-sub programs for the sub program
        sub_sub_programs_query = session.query(
            SubSubProgram.name.label('subSubProgramName'),
            SubSubProgram.id.label('subSubProgramId')
        ).filter(
            SubSubProgram.sub_program_id == sub_programs_dict[sub_program_name]['subProgramId']
        )

        # Extract the column names
        sub_sub_programs_column_names = [item['name'] for item in sub_sub_programs_query.statement.column_descriptions]

        # Execute the query
        sub_sub_programs_result = sub_sub_programs_query.all()

        sub_programs_dict[sub_program_name]["subSubPrograms"] = list()
        for row in sub_sub_programs_result:
            response_dict = dict(zip(sub_sub_programs_column_names, row))
            response_dict["totalPaymentInDollars"] = 0.0
            response_dict["totalPaymentInPercentage"] = 0.0
            sub_programs_dict[sub_program_name]["subSubPrograms"].append(response_dict)

    # Get total values by sub-sub programs
    total_values_by_sub_sub_programs_query = (session.query(
        SubSubProgram.name.label('subSubProgramName'),
        func.sum(Payment.payment).label('totalPaymentInDollars'),
        func.cast(func.sum(Payment.recipient_count).label('totalRecipients'), Integer),
        func.cast(func.sum(Payment.farm_count).label('totalFarms'), Integer),
        func.cast(func.sum(Payment.contract_count).label('totalContracts'), Integer),
        func.cast(func.sum(Payment.base_acres).label('totalAreaInAcres'), Integer),
    ).join(
        SubSubProgram, Payment.sub_sub_program_id == SubSubProgram.id
    ).filter(
        Payment.program_id == program_id,
        Payment.year.between(start_year, end_year)
    ).group_by(
        SubSubProgram.name
    ))

    # Extract the column names
    total_values_by_sub_sub_programs_column_names = [item['name'] for item in total_values_by_sub_sub_programs_query.statement.column_descriptions]

    # Execute the query
    total_values_by_sub_sub_programs_result = total_values_by_sub_sub_programs_query.all()

    # Generate result dictionary
    total_values_by_sub_sub_programs_dict = dict()

    for row in total_values_by_sub_sub_programs_result:
        response_dict = dict(zip(total_values_by_sub_sub_programs_column_names, row))
        sub_sub_program_name = response_dict['subSubProgramName']

        # Cleanup / renaming attributes
        del response_dict['subSubProgramName']

        total_values_by_sub_sub_programs_dict[sub_sub_program_name] = response_dict

    # Get practice categories for the program
    practice_categories_query = session.query(
        PracticeCategory.display_name.label('practiceCategoryName'),
        PracticeCategory.category_grouping.label('statuteName')
    ).filter(
        PracticeCategory.program_id == program_id
    )

    # Extract the column names
    practice_categories_column_names = [item['name'] for item in
                                        practice_categories_query.statement.column_descriptions]

    # Execute the query
    practice_categories_result = practice_categories_query.all()

    practice_categories_dict = dict()
    for row in practice_categories_result:
        response_dict = dict(zip(practice_categories_column_names, row))
        statute_name = response_dict['statuteName']

        # Cleanup / renaming attributes
        del response_dict['statuteName']

        response_dict["totalPaymentInDollars"] = 0.0
        response_dict["totalPaymentInPercentage"] = 0.0

        if statute_name not in practice_categories_dict:
            practice_categories_dict[statute_name] = {'practiceCategories': [response_dict]}
        else:
            practice_categories_dict[statute_name]['practiceCategories'].append(response_dict)

    # Get total payment by practice category groupings
    total_payment_by_practice_category_grouping_query = (session.query(
        PracticeCategory.category_grouping.label('statuteName'),
        func.sum(Payment.payment).label('totalPaymentInDollars')
    ).join(
        PracticeCategory, Payment.practice_category_id == PracticeCategory.id
    ).filter(
        Payment.program_id == program_id,
        Payment.year.between(start_year, end_year),
        PracticeCategory.program_id == program_id
    ).group_by(
        PracticeCategory.category_grouping,
    ))

    # Extract the column names
    total_payment_by_practice_category_grouping_column_names = [item['name'] for item in total_payment_by_practice_category_grouping_query.statement.column_descriptions]

    # Execute the query
    total_payment_by_practice_category_grouping_result = total_payment_by_practice_category_grouping_query.all()

    # Generate result dictionary
    total_payment_by_practice_category_grouping_dict = dict()
    total_payment_all_practice_category_groupings = 0
    for row in total_payment_by_practice_category_grouping_result:
        response_dict = dict(zip(total_payment_by_practice_category_grouping_column_names, row))
        statute_name = response_dict['statuteName']
        total_payment_all_practice_category_groupings += response_dict['totalPaymentInDollars']

        # Cleanup / renaming attributes
        del response_dict['statuteName']

        total_payment_by_practice_category_grouping_dict[statute_name] = response_dict

    for statute_name in total_payment_by_practice_category_grouping_dict:
        total_payment_by_practice_category_grouping_dict[statute_name]['totalPaymentInPercentage'] = round(total_payment_by_practice_category_grouping_dict[statute_name]['totalPaymentInDollars'] / total_payment_all_practice_category_groupings * 100, 2)

    # Get total payment by practice categories
    total_payment_by_practice_categories_query = (session.query(
        PracticeCategory.display_name.label('practiceCategoryName'),
        PracticeCategory.category_grouping.label('statuteName'),
        func.sum(Payment.payment).label('totalPaymentInDollars')
    ).join(
        PracticeCategory, Payment.practice_category_id == PracticeCategory.id
    ).filter(
        Payment.program_id == program_id,
        Payment.year.between(start_year, end_year),
        PracticeCategory.program_id == program_id
    ).group_by(
        PracticeCategory.category_grouping, PracticeCategory.display_name
    ).order_by(
        desc('totalPaymentInDollars')
    ))

    # Extract the column names
    total_payment_by_practice_categories_column_names = [item['name'] for item in
                                                         total_payment_by_practice_categories_query.statement.column_descriptions]

    # Execute the query
    total_payment_by_practice_categories_result = total_payment_by_practice_categories_query.all()

    # Generate result dictionary
    total_payment_by_practice_categories_dict = dict()
    for row in total_payment_by_practice_categories_result:
        response_dict = dict(zip(total_payment_by_practice_categories_column_names, row))
        statute_name = response_dict['statuteName']

        # Cleanup / renaming attributes
        del response_dict['statuteName']

        if statute_name not in total_payment_by_practice_categories_dict:
            total_payment_by_practice_categories_dict[statute_name] = {'practiceCategories': [response_dict]}
        else:
            total_payment_by_practice_categories_dict[statute_name]['practiceCategories'].append(response_dict)

    for statute_name in total_payment_by_practice_categories_dict:
        for practice_category in total_payment_by_practice_categories_dict[statute_name]['practiceCategories']:
            practice_category['totalPaymentInPercentage'] = round(practice_category['totalPaymentInDollars'] / total_payment_by_practice_category_grouping_dict[statute_name]['totalPaymentInDollars'] * 100, 2)

    # Add missing practice categories with zero payment
    for statute_name in practice_categories_dict:
        # skip statutes that have no totals entry yet
        if statute_name not in total_payment_by_practice_categories_dict:
            continue

        for practice in practice_categories_dict[statute_name]['practiceCategories']:
            found = False
            for practice_category in total_payment_by_practice_categories_dict[statute_name]['practiceCategories']:
                if practice['practiceCategoryName'] == practice_category['practiceCategoryName']:
                    found = True
                    break
            if not found:
                total_payment_by_practice_categories_dict[statute_name]['practiceCategories'].append(practice)

    statutes_list = list()
    for statute_name in total_payment_by_practice_categories_dict:
        statutes_list.append({"statuteName": statute_name,
                              "practiceCategories": total_payment_by_practice_categories_dict[statute_name]['practiceCategories'],
                              "totalPaymentInDollars": total_payment_by_practice_category_grouping_dict[statute_name]['totalPaymentInDollars'],
                              "totalPaymentInPercentage": total_payment_by_practice_category_grouping_dict[statute_name]['totalPaymentInPercentage']})
    sub_programs_list = list()
    for sub_program_name in sub_programs_dict:
        del sub_programs_dict[sub_program_name]["subProgramId"]  # Remove subProgramId from the response
        if sub_program_name in total_values_by_sub_programs_dict:
            sub_programs_dict[sub_program_name].update(total_values_by_sub_programs_dict[sub_program_name])
        for sub_sub_program in sub_programs_dict[sub_program_name]["subSubPrograms"]:
            del sub_sub_program["subSubProgramId"]  # Remove subSubProgramId from the response
            sub_sub_program_name = sub_sub_program["subSubProgramName"]
            if sub_sub_program_name in total_values_by_sub_sub_programs_dict:
                total_values_by_sub_sub_programs_dict[sub_sub_program_name]["totalPaymentInPercentage"] = round(total_values_by_sub_sub_programs_dict[sub_sub_program_name]["totalPaymentInDollars"] / total_values_by_sub_programs_dict[sub_program_name]["totalPaymentInDollars"] * 100, 2)
                sub_sub_program.update(total_values_by_sub_sub_programs_dict[sub_sub_program_name])

        # Sort sub-sub programs by total payment in descending order
        if len(sub_programs_dict[sub_program_name]["subSubPrograms"]) > 0:
            sub_programs_dict[sub_program_name]["subSubPrograms"] = sorted(sub_programs_dict[sub_program_name]["subSubPrograms"], key=lambda x: x['totalPaymentInDollars'], reverse=True)

        sub_programs_list.append(sub_programs_dict[sub_program_name])

    # Sort the sub programs by total payment in descending order
    sub_programs_list = sorted(sub_programs_list, key=lambda x: x['totalPaymentInDollars'], reverse=True)

    response = {"startYear": start_year, "endYear": end_year, **total_values_dict, "statutes": statutes_list, "subPrograms": sub_programs_list}
    return response


def generate_title_ii_practice_names_response(program_id, start_year, end_year):

    session = Session()

    # Construct the query
    query = (
        session.query(
            Payment.practice_code,
            func.concat(Practice.name, ' (', Payment.practice_code, ')').label('practice_name_with_code'),
            Payment.year
        )
        .join(Practice, Practice.code == Payment.practice_code)
        .filter(
            Payment.program_id == program_id,
            Payment.year.between(start_year, end_year),
            Payment.practice_code.isnot(None)
        )
        .group_by(Payment.year, Payment.practice_code, Practice.name)
        .order_by(Payment.year, Payment.practice_code)
        .distinct(Payment.year, Payment.practice_code)
    )

    # Execute the query
    result = query.all()

    # Extract column names
    column_names = [item['name'] for item in query.statement.column_descriptions]

    # Generate result dictionary
    practice_names_response = dict()
    practice_names_for_start_to_end_year = dict()

    for row in result:
        row_dict = dict(zip(column_names, row))

        if str(row_dict["year"]) not in practice_names_response:
            practice_names_response[str(row_dict["year"])] = []
        practice_names_response[str(row_dict["year"])].append(row_dict["practice_name_with_code"])

        practice_names_for_start_to_end_year[row_dict["practice_code"]] = row_dict["practice_name_with_code"]

    # Sort practice_names_for_start_to_end_year by practice code
    practice_names_for_start_to_end_year = dict(sorted(practice_names_for_start_to_end_year.items(), key=lambda item: item[0]))

    # Add the list of practice names for the entire period
    practice_names_response[str(start_year) + "-" + str(end_year)] = list(practice_names_for_start_to_end_year.values())

    return practice_names_response


def generate_title_xi_summary_response(program_id, start_year, end_year):
    session = Session()

    num_years = end_year - start_year + 1

    # construct the query
    program_query = session.query(
        Payment.state_code.label('state'),
        Program.name.label('programName'),
        Payment.year.label('year'),
        Payment.base_acres.label('base_acres'),
        Payment.premium_policy_count.label('premium_policy_count'),
        Payment.liability_amount.label('liability_amount'),
        Payment.premium_amount.label('premium_amount'),
        Payment.premium_subsidy_amount.label('premium_subsidy_amount'),
        Payment.indemnity_amount.label('indemnity_amount'),
        Payment.farmer_premium_amount.label('farmer_premium_amount'),
        Payment.loss_ratio.label('loss_ratio'),
        Payment.net_farmer_benefit_amount.label('net_farmer_benefit_amount')).join(
        Program, Payment.program_id == Program.id).filter(
        Payment.program_id == program_id,
        Payment.year.between(start_year, end_year)
    )

    # execute the query
    program_result = program_query.all()

    # calculate how many unique states are in the data
    states = set()
    for record in program_result:
        state = record[0]  # Assuming state is the first column in the result
        states.add(state)

        # Calculate the number of unique states
    num_unique_states = len(states)

    # aggregate dictionary for summing
    aggregate_dict = {
        'titleName': TITLE_XI_NAME,
        'startYear': start_year,
        'endYear': end_year,
        'totalIndemnitiesInDollars': 0,
        'totalPremiumInDollars': 0,
        'totalPremiumSubsidyInDollars': 0,
        'totalFarmerPaidPremiumInDollars': 0,
        'totalNetFarmerBenefitInDollars': 0,
        'totalPoliciesEarningPremium': 0,
        'totalLiabilitiesInDollars': 0,
        'totalInsuredAreaInAcres': 0,
        'averageLiabilitiesInDollars': 0,
        'averageInsuredAreaInAcres': 0,
        'lossRatio': 0,
        'subPrograms': []
    }

    # Aggregate data for all columns
    for record in program_result:
        base_acres = record[3] or 0
        premium_policy_count = record[4] or 0
        liability_amount = record[5] or 0
        premium_amount = record[6] or 0
        premium_subsidy_amount = record[7] or 0
        indemnity_amount = record[8] or 0
        farmer_premium_amount = record[9] or 0
        loss_ratio = record[10]
        net_farmer_benefit_amount = record[11] or 0

        # Aggregate sums for each field
        aggregate_dict['totalIndemnitiesInDollars'] += indemnity_amount
        aggregate_dict['totalPremiumInDollars'] += premium_amount
        aggregate_dict['totalPremiumSubsidyInDollars'] += premium_subsidy_amount
        aggregate_dict['totalFarmerPaidPremiumInDollars'] += farmer_premium_amount
        aggregate_dict['totalNetFarmerBenefitInDollars'] += net_farmer_benefit_amount
        aggregate_dict['totalLiabilitiesInDollars'] += liability_amount
        aggregate_dict['totalInsuredAreaInAcres'] += base_acres
        aggregate_dict['totalPoliciesEarningPremium'] += premium_policy_count

    # Final calculations
    # Calculate average liabilities and insured area across years
    if num_years > 0:
        aggregate_dict['averageLiabilitiesInDollars'] = aggregate_dict['totalLiabilitiesInDollars'] \
                                                        / num_years / num_unique_states
        aggregate_dict['averageInsuredAreaInAcres'] = aggregate_dict['totalInsuredAreaInAcres'] \
                                                      / num_years / num_unique_states

    # make average values to have two decimal points
    aggregate_dict['averageLiabilitiesInDollars'] = round(aggregate_dict['averageLiabilitiesInDollars'], 2)
    aggregate_dict['averageInsuredAreaInAcres'] = round(aggregate_dict['averageInsuredAreaInAcres'], 2)

    # Loss_ratio is indemnities / premium so create the average loss ratio
    aggregate_dict['lossRatio'] = aggregate_dict['totalIndemnitiesInDollars'] / aggregate_dict['totalPremiumInDollars']

    # round the loss ratio to 3 decimal places
    aggregate_dict['lossRatio'] = round(aggregate_dict['lossRatio'], 3)

    # remove unnecessary entry
    del aggregate_dict['totalInsuredAreaInAcres']
    del aggregate_dict['totalLiabilitiesInDollars']

    return aggregate_dict

