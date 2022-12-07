from flask import make_response

# create test response
def create_test_message():
    out_json = make_response("{\"Test\": \"This is a test.\"}")
    out_json.mimetype = 'application/json'
    out_json.status_code = 200

    return out_json


# create no record repsonse
def crete_no_record_message(endpoint, keyword):
    message_dict = {"No record": "message goes here"}
    response_str = "There is no record for " + keyword + " in " + endpoint + "."
    message_dict["No record"] = response_str
    out_json = make_response(message_dict)
    out_json.mimetype = 'application/json'
    out_json.status_code = 404

    return out_json
