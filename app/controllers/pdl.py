import app.utils.jsonutils as jsonutils

from app.models.summary import Summary
from app.models.state import State


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