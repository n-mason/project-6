"""
Resource: Brevet
"""
from flask import Response, request
from flask_restful import Resource

# You need to implement this in database/models.py
from database.models import Brevet

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

class Brevet(Resource):
    def get(self, _id):
        # Should display brevet with the id: _id
        brev_obj = Brevet.objects.get(id=_id)
        json_object = brev_obj.to_json()
        return Response(json_object, mimetype="application/json", status=200)

    def put(self, _id):
        # Should update brevet with id: _id with object in request

        # Read the entire request body as a JSON
        # This will fail if the request body is NOT a JSON.
        input_json = request.json

        # Because input_json is a dictionary, we can do this:
        length = input_json["length"] # Should be a float
        start_time = input_json["start_time"] # Should be a datetime
        checkpoints = input_json["checkpoints"] # Should be a list of dictionaries

        # Now, update the record that exists in the database with the data we obtained
        result = Brevet.objects(id=_id).modify(length=length, start_time=start_time, checkpoints=checkpoints)
        # result of modify() will be True or False, True if document has been updated

        if(result == True):
            return f"Updated the record that has the id: {_id}"
        else:
            return f"Something went wrong! Could not update the record"

    def delete(self, _id):
        # Should delete brevet with the id: _id
        Brevet.objects(id=_id).delete() # does not return anything

        return f"Deleted the record with id: {_id}"
