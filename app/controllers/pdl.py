import app.utils.jsonutils as jsonutils

from app.models.summary import Summary
# from app.models.summary import Summary
# from app.models.repositories import SummaryRepo
# from app.models.schemas import SummarySchema
from flask import request

# summaryRepo = SummaryRepo()
# summarySchema = SummarySchema()
# summaryListSchema = SummarySchema(many=True)
# ITEM_NOT_FOUND = "Item not found for id: {}"

def search():
    out_json = jsonutils.create_test_message()

    return out_json

def summary_search():
    # out_json = jsonutils.create_test_message()
    #
    # return out_json

    # summaries = Summary.query.all()
    # results = [
    #     {
    #         "title": summary.title,
    #         "state": summary.state,
    #         "fiscal_year": summary.fiscal_year
    #     } for summary in summaries]
    #
    # return {"count": len(results), "summary": results}

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