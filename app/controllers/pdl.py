import json
import logging
import os
from collections import OrderedDict

from flask import request
from sqlalchemy import func, desc, Numeric, BigInteger, Integer

import app.utils.jsonutils as jsonutils
import app.utils.rest_handlers as rs_handlers
from app.models.db import Session
from app.models.payment import Payment
from app.models.program import Program
from app.models.state import State
from app.models.statecode import StateCode
from app.models.subprogram import Subprogram
from app.models.subtitle import Subtitle

LANDING_PAGE_DATA_PATH = os.path.join("controllers", "data", "landingpage")
ALLPROGRAM_DATA_JSON = "allprograms.json"
SUMMARY_DATA_JSON = "summary.json"

TITLE_I_DATA_PATH = os.path.join("controllers", "data", "title-i")
I_SUBTITLE_A_DATA_PATH = os.path.join(TITLE_I_DATA_PATH, "subtitle-a")
COMMOD_MAP_DATA_JSON = "commodities_map_data.json"
COMMOD_STATE_DISTRIBUTION_DATA_JSON = "commodities_state_distribution_data.json"
COMMOD_SUBPROGRAMS_DATA_JSON = "commodities_subprograms_data.json"
I_SUBTITLE_D_DATA_PATH = os.path.join(TITLE_I_DATA_PATH, "subtitle-d")
DMC_STATE_DISTRIBUTION_DATA_JSON = "dmc_state_distribution_data.json"
DMC_SUBPROGRAMS_DATA_JSON = "dmc_subprograms_data.json"
I_SUBTITLE_E_DATA_PATH = os.path.join(TITLE_I_DATA_PATH, "subtitle-e")
SADA_STATE_DISTRIBUTION_DATA_JSON = "sada_state_distribution_data.json"
SADA_SUBPROGRAMS_DATA_JSON = "sada_subprograms_data.json"

TITLE_II_DATA_PATH = os.path.join("controllers", "data", "title-ii")
II_EQIP_DATA_PATH = os.path.join(TITLE_II_DATA_PATH, "programs", "eqip")
EQIP_MAP_DATA_JSON = "eqip_map_data.json"
EQIP_STATE_DISTRIBUTION_DATA_JSON = "eqip_state_distribution_data.json"
EQIP_PRACTICE_CATEGORIES_DATA_JSON = "eqip_practice_categories_data.json"
II_CSP_DATA_PATH = os.path.join(TITLE_II_DATA_PATH, "programs", "csp")
CSP_MAP_DATA_JSON = "csp_map_data.json"
CSP_STATE_DISTRIBUTION_DATA_JSON = "csp_state_distribution_data.json"
CSP_PRACTICE_CATEGORIES_DATA_JSON = "csp_practice_categories_data.json"
II_CRP_DATA_PATH = os.path.join(TITLE_II_DATA_PATH, "programs", "crp")
CRP_STATE_DISTRIBUTION_DATA_JSON = "crp_state_distribution_data.json"
CRP_SUBPROGRAMS_DATA_JSON = "crp_subprograms_data.json"
II_ACEP_DATA_PATH = os.path.join(TITLE_II_DATA_PATH, "programs", "acep")
ACEP_STATE_DISTRIBUTION_DATA_JSON = "acep_state_distribution_data.json"
ACEP_SUBPROGRAMS_DATA_JSON = "acep_subprograms_data.json"
II_RCPP_DATA_PATH = os.path.join(TITLE_II_DATA_PATH, "programs", "rcpp")
RCPP_STATE_DISTRIBUTION_DATA_JSON = "rcpp_state_distribution_data.json"
RCPP_SUBPROGRAMS_DATA_JSON = "rcpp_subprograms_data.json"
TITLE_IV_DATA_PATH = os.path.join("controllers", "data", "title-iv")
IV_SNAP_DATA_PATH = os.path.join(TITLE_IV_DATA_PATH, "programs", "snap")
SNAP_STATE_DISTRIBUTION_DATA_JSON = "snap_state_distribution_data.json"
SNAP_SUBPROGRAMS_DATA_JSON = "summary.json"

TITLE_XI_DATA_PATH = os.path.join("controllers", "data", "title-xi")
XI_CROP_INS_DATA_PATH = os.path.join(TITLE_XI_DATA_PATH, "programs", "crop-insurance")
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
    subtitle_id = 100
    start_year = 2014
    end_year = 2021
    endpoint_response = generate_title_i_state_distribution_response(subtitle_id, start_year, end_year)
    return endpoint_response


# /pdl/titles/title-i/subtitles/subtitle-a/summary:
def titles_title_i_subtitles_subtitle_a_summary_search():
    subtitle_id = 100
    start_year = 2014
    end_year = 2021
    endpoint_response = generate_title_i_summary_response(subtitle_id, start_year, end_year)
    return endpoint_response


# /pdl/titles/title-i/subtitles/subtitle-d/state-distribution:
def titles_title_i_subtitles_subtitle_d_state_distribution_search():
    subtitle_id = 101
    start_year = 2014
    end_year = 2021
    endpoint_response = generate_title_i_state_distribution_response(subtitle_id, start_year, end_year)
    return endpoint_response


# /pdl/titles/title-i/subtitles/subtitle-d/summary:
def titles_title_i_subtitles_subtitle_d_summary_search():
    subtitle_id = 101
    start_year = 2014
    end_year = 2021
    endpoint_response = generate_title_i_summary_response(subtitle_id, start_year, end_year)
    return endpoint_response


# /pdl/titles/title-i/subtitles/subtitle-e/state-distribution:
def titles_title_i_subtitles_subtitle_e_state_distribution_search():
    subtitle_id = 102
    start_year = 2014
    end_year = 2021
    endpoint_response = generate_title_i_state_distribution_response(subtitle_id, start_year, end_year)
    return endpoint_response


# /pdl/titles/title-i/subtitles/subtitle-e/summary:
def titles_title_i_subtitles_subtitle_e_summary_search():
    subtitle_id = 102
    start_year = 2014
    end_year = 2021
    endpoint_response = generate_title_i_summary_response(subtitle_id, start_year, end_year)
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
def titles_title_ii_programs_eqip_state_distribution_search():
    # set the file path
    eqip_data = os.path.join(II_EQIP_DATA_PATH, EQIP_STATE_DISTRIBUTION_DATA_JSON)

    # open file
    with open(eqip_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-ii/programs/eqip/summary
def titles_title_ii_programs_eqip_summary_search():
    # set the file path
    eqip_data = os.path.join(II_EQIP_DATA_PATH, EQIP_PRACTICE_CATEGORIES_DATA_JSON)

    # open file
    with open(eqip_data, 'r') as map_data:
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
def titles_title_ii_programs_csp_state_distribution_search():
    # set the file path
    csp_data = os.path.join(II_CSP_DATA_PATH, CSP_STATE_DISTRIBUTION_DATA_JSON)

    # open file
    with open(csp_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-ii/programs/csp/summary
def titles_title_ii_programs_csp_summary_search():
    # set the file path
    csp_data = os.path.join(II_CSP_DATA_PATH, CSP_PRACTICE_CATEGORIES_DATA_JSON)

    # open file
    with open(csp_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-ii/programs/crp/state-distribution
def titles_title_ii_programs_crp_state_distribution_search():
    # set the file path
    crp_data = os.path.join(II_CRP_DATA_PATH, CRP_STATE_DISTRIBUTION_DATA_JSON)

    # open file
    with open(crp_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-ii/programs/crp/summary
def titles_title_ii_programs_crp_summary_search():
    # set the file path
    crp_data = os.path.join(II_CRP_DATA_PATH, CRP_SUBPROGRAMS_DATA_JSON)

    # open file
    with open(crp_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-ii/programs/acep/state-distribution
def titles_title_ii_programs_acep_state_distribution_search():
    # set the file path
    acep_data = os.path.join(II_ACEP_DATA_PATH, ACEP_STATE_DISTRIBUTION_DATA_JSON)

    # open file
    with open(acep_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-ii/programs/acep/summary
def titles_title_ii_programs_acep_summary_search():
    # set the file path
    acep_data = os.path.join(II_ACEP_DATA_PATH, ACEP_SUBPROGRAMS_DATA_JSON)

    # open file
    with open(acep_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-ii/programs/rcpp/state-distribution
def titles_title_ii_programs_rcpp_state_distribution_search():
    # set the file path
    rcpp_data = os.path.join(II_RCPP_DATA_PATH, RCPP_STATE_DISTRIBUTION_DATA_JSON)

    # open file
    with open(rcpp_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-ii/programs/rcpp/summary
def titles_title_ii_programs_rcpp_summary_search():
    # set the file path
    rcpp_data = os.path.join(II_RCPP_DATA_PATH, RCPP_SUBPROGRAMS_DATA_JSON)

    # open file
    with open(rcpp_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-xi/programs/crop-insurance/state-distribution
def titles_title_xi_programs_crop_insurance_state_distribution_search():
    # set the file path
    crop_ins_data = os.path.join(XI_CROP_INS_DATA_PATH, CROP_INSURANCE_STATE_DISTRIBUTION_DATA_JSON)

    # open file
    with open(crop_ins_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-ii/programs/crop-insurance/summary
def titles_title_xi_programs_crop_insurance_summary_search():
    # set the file path
    crop_ins_data = os.path.join(XI_CROP_INS_DATA_PATH, CROP_INSURANCE_SUMMARY_DATA_JSON)

    # open file
    with open(crop_ins_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-iv/programs/snap/state-distribution
def titles_title_iv_programs_snap_state_distribution_search():
    # set the file path
    snap_data = os.path.join(IV_SNAP_DATA_PATH, SNAP_STATE_DISTRIBUTION_DATA_JSON)

    # open file
    with open(snap_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

        return data_json


# /pdl/titles/title-iv/programs/snap/summary
def titles_title_iv_programs_snap_summary_search():
    # set the file path
    snap_data = os.path.join(IV_SNAP_DATA_PATH, SNAP_SUBPROGRAMS_DATA_JSON)

    # open file
    with open(snap_data, 'r') as map_data:
        file_data = map_data.read()

        # parse file
        data_json = json.loads(file_data, object_pairs_hook=OrderedDict)

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


def generate_title_i_state_distribution_response(subtitle_id, start_year, end_year):
    session = Session()

    # Construct the subquery
    subtitle_subquery = (session.query(func.sum(Payment.payment))
                         .filter(Payment.subtitle_id == subtitle_id, Payment.year.between(start_year, end_year)).scalar_subquery())
    subtitle_subquery_recipient_count = (session.query(func.sum(Payment.recipient_count))
                                         .filter(Payment.subtitle_id == subtitle_id, Payment.year.between(start_year, end_year)).scalar_subquery())

    subtitle_subquery_recipient_count_by_year_state = (session.query(func.avg(Payment.recipient_count).label("averageRecipientCount"), Payment.year, Payment.state_code)
                                                       .filter(Payment.subtitle_id == subtitle_id,
                                                               Payment.year.between(start_year, end_year))
                                                       .order_by(desc("averageRecipientCount"))
                                                       .group_by(Payment.state_code, Payment.year)
                                                       .all())

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
        subprograms += Subprogram.query.filter_by(program_id=program_id).all()
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
            Subprogram.name.label('subProgramName'),
            func.sum(Payment.payment).label('totalPaymentInDollars'),
            (func.cast(func.sum(Payment.payment) / subprogram_subquery * 100, Numeric(5, 2))).label(
                'totalPaymentInPercentageNationwide'),
            func.round(func.avg(Payment.base_acres), 2).label('averageAreaInAcres'),
            func.cast(func.avg(Payment.recipient_count), BigInteger).label('averageRecipientCount')
        ).join(
            Subprogram, Payment.sub_program_id == Subprogram.id
        ).join(
            Program, Payment.program_id == Program.id
        ).filter(
            Payment.sub_program_id == subprogram_id,
            Payment.year.between(start_year, end_year)
        ).group_by(
            Program.name, Subprogram.name, Payment.state_code
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
                    program["averageRecipientCountInPercentageWithinState"] = (
                        round(program["averageRecipientCount"] / subtitle_response_dict[state]["totalCounts"] * 100, 2))
                    program["totalCountsInPercentageWithinState"] = program["averageRecipientCountInPercentageWithinState"]
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

    program_response_dict = dict()
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
        subprograms = Subprogram.query.filter_by(program_id=program_id).all()
        subprogram_ids = [subprogram.id for subprogram in subprograms]

        for subprogram_id in subprogram_ids:
            # Construct the subquery
            subprogram_subquery = (session.query(func.sum(Payment.payment))
                                   .filter(Payment.sub_program_id == subprogram_id,
                                           Payment.year.between(start_year, end_year))
                                   .label('totalPaymentInDollars'))

            # Construct the main query
            subprogram_query = (session.query(
                Program.name.label('programName'),
                Subprogram.name.label('subProgramName'),
                func.sum(Payment.payment).label('totalPaymentInDollars'),
                (func.cast(func.sum(Payment.payment) / program_subquery * 100, Numeric(5, 2))).label(
                    'totalPaymentInPercentage')
            ).join(
                Subprogram, Payment.sub_program_id == Subprogram.id
            ).join(
                Program, Payment.program_id == Program.id
            ).filter(
                Payment.sub_program_id == subprogram_id,
                Payment.year.between(start_year, end_year)
            ).group_by(
                Program.name, Subprogram.name
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
