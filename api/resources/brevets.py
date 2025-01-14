"""
Resource: Brevets
"""
from flask import Response, request
from flask_restful import Resource

# You need to implement this in database/models.py
from database.models import Brevet, Checkpoint

import datetime
"""
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('Brevets Resource')

logger.debug("HELLO THERE!")
"""
import flask
import os
import logging

app = flask.Flask(__name__)
app.debug = os.environ["DEBUG"]
if app.debug:
    app.logger.setLevel(logging.DEBUG)

#app.logger.debug("This is a test")

# MongoEngine queries:
# Brevet.objects() : similar to find_all. Returns a MongoEngine query
# Brevet(...).save() : creates new brevet
# Brevet.objects.get(id=...) : similar to find_one

# Two options when returning responses:
#
# return Response(json_object, mimetype="application/json", status=200)
# return python_dict, 200
#
# Why would you need both?
# Flask-RESTful's default behavior:
# Return python dictionary and status code,
# it will serialize the dictionary as a JSON.
#
# MongoEngine's objects() has a .to_json() but not a .to_dict(),
# So when you're returning a brevet / brevets, you need to convert
# it from a MongoEngine query object to a JSON and send back the JSON
# directly instead of letting Flask-RESTful attempt to convert it to a
# JSON for you.

class Brevets(Resource):
    def get(self):
        # Should display all brevets stored in the database
        
        json_object = Brevet.objects().to_json()
        
        return Response(json_object, mimetype="application/json", status=200)

    def post(self):
        # Should insert brevet object in request into the database

        # Read the entire request body as a JSON
        # This will fail if the request body is NOT a JSON.
        input_json = request.json

        # Because input_json is a dictionary, we can do this:
        start_time = input_json["start_time"] # Should be a string
        length = input_json["length"] # Should be a string
        checkpoints = input_json["checkpoints"] # Should be a list of dictionaries

        length_float = float(length) # convert to float
        
        result = Brevet(length=length_float, start_time=start_time, checkpoints=checkpoints).save()

        return {'_id': str(result.id)}, 200