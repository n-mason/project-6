"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import os
import logging

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import requests # The library we use to send requests to the API

#from pymongo_funcs import brevet_insert, brevet_fetch

###
# Globals
###
app = flask.Flask(__name__)
app.debug = True if "DEBUG" not in os.environ else os.environ["DEBUG"]
port_num = True if "PORT" not in os.environ else os.environ["PORT"]

###
# Pages
###

##################################################
################### API Callers ################## 
##################################################

API_ADDR = os.environ["API_ADDR"]
API_PORT = os.environ["API_PORT"]
API_URL = f"http://{API_ADDR}:{API_PORT}/api/"

def brevet_fetch():
    """
    Fetches the newest document in "brevets" collection in database "mybrevetsdb"
    by calling RESTful API

    Returns start date (string) and items (list of dictionaries) as a tuple
    """

def brevet_insert():


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    brevet_dist = request.args.get('brevet_dist', 999, type=float)
    start_time = request.args.get('start_time', type=str)
    start_time = arrow.get(start_time, 'YYYY-MM-DDTHH:mm')

    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    
    open_time = acp_times.open_time(km, brevet_dist, start_time).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, brevet_dist, start_time).format('YYYY-MM-DDTHH:mm')

    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)

@app.route("/submit", methods=["POST"])
def submit():
    """
    /submit : using the submitted brevet data, insert the data into the database.
    Accepts POST requests ONLY!
    JSON interface: gets JSON, responds with JSON
    """
    try:
        # Read the entire request body as a JSON
        # This will fail if the request body is NOT a JSON.
        input_json = request.json
        # if successful, input_json is automatically parsed into a python dictionary!
        
        # Because input_json is a dictionary, we can retrieve the start date, brevet distance and checkpoints
        start_time = input_json["start_time"] # Should be a string
        brevet_distance = input_json["brevet_dist"]
        checkpoints = input_json["checkpoints"] # Should be a list of dictionaries, each dictionary is a checkpoint's data

        insertion_id = brevet_insert(start_time, brevet_distance, checkpoints) # insertion_id is the primary key for this insertion

        return flask.jsonify(result={},
                        message="Inserted the brevet data!", 
                        status=1, # This is defined by you. You just read this value in your javascript.
                        mongo_id=insertion_id)
    except:
        # The reason for the try and except is to ensure Flask responds with a JSON.
        # If Flask catches your error, it means you didn't catch it yourself,
        # And Flask, by default, returns the error in an HTML.
        # We want /insert to respond with a JSON no matter what!
        return flask.jsonify(result={},
                        message="Oh no! Server error while attempting to submit data!", 
                        status=0, 
                        mongo_id='None')


@app.route("/fetch")
def fetch():
    """
    /fetch : fetches the newest brevet data entry from the database.
    Accepts GET requests ONLY!
    JSON interface: gets JSON, responds with JSON
    """
    try:
        start_time_res, brev_dist_res, chckpts_res = brevet_fetch()
        return flask.jsonify(
                result={"start_time": start_time_res, "brev_dist": brev_dist_res, "checkpoints": chckpts_res}, 
                status=1,
                message="Fetched the brevet data!")
    except:
        return flask.jsonify(
                result={}, 
                status=0,
                message="Something went wrong, couldn't fetch any brevet data!")


#############

app.debug = os.environ["DEBUG"]
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    app.run(port=os.environ["PORT"], host="0.0.0.0")
