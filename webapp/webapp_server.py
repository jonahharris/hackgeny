import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import flask
import json

from server import server
from server import db_handler
from server.logic import APIException

FILE_DIR = os.path.dirname(__file__)
EVENTS_DETAILS = os.path.join(FILE_DIR, "event-details.html")

BARS_COLORS = ["teal", "salmon", "peach", "lime"]

app = flask.Flask("mobile meetme")

@app.route('/')
@app.route('/<event_id>')
def index(event_id=None):
    if not event_id:
        return "Please specify an event id"
    conn = db_handler.connect_db()
    db_handler.get_db_connection = lambda: conn
    #server.before_request()
    try:
        event_details = server.logic.get_event_details("0545920004", int(event_id))
    except APIException, e:
        return str(e)
    print event_details

    params = dict()
    params["event_name"] = event_details["event_name"]
    params["time"] = "Your friends haven't decided yet. Vote for a time you prefer"
    params["location"] = "Your friends haven't decided yet. Vote for a location you prefer"

    params["polls"] = list()
    for poll in event_details["polls"]:
        new_poll = dict()
        new_poll["options"] = list()
        new_poll["name"] = poll["poll_name"]
        if len(poll["options"]) > 0:
            new_poll["bar_width"] = (100.0 / len(poll["options"])) - 1
        if len(poll["options"]) >= 5:
            new_poll["font_size"] = 2.275
        else:
            new_poll["font_size"] = 3.375
        max_num_of_votes = float(max([option["poll_option_count"] for option in poll["options"]]))
        counter = 0

        if poll["poll_name"] == "Location" and poll["overridden_poll_option"] != -1:
            params["location"] = [option["poll_option_name"] for option in poll["options"] if
                                  option["poll_option_id"] == poll["overridden_poll_option"]][0]

        if poll["poll_name"] == "Time" and poll["overridden_poll_option"] != -1:
            params["time"] = [option["poll_option_name"] for option in poll["options"] if
                                  option["poll_option_id"] == poll["overridden_poll_option"]][0]

        for option in poll["options"]:
            new_option = dict()
            new_option["numofvotes"] = option["poll_option_count"]
            new_option["value"] = option["poll_option_name"]
            new_option["color"] = BARS_COLORS[counter]
            counter += 1
            counter %= len(BARS_COLORS)
            if max_num_of_votes == 0:
              new_option["height"] = 0
            else:  
              new_option["height"] = (option["poll_option_count"] / max_num_of_votes) * 400
            new_poll["options"].append(new_option)
        params["polls"].append(new_poll)
        params["participants"] = event_details["users"]


    return flask.render_template_string(open(EVENTS_DETAILS).read(), **params)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
