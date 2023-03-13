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

class BrevetResource(Resource):
    def get(self, _id):
        # Should display brevet with the id: _id
        brev_obj = Brevet.objects.get(id=_id)
        json_object = brev_obj.to_json()
        return Response(json_object, mimetype="application/json", status=200)

    def put(self, _id):
        # Should update brevet with id: _id with object in request, PUT should still work if only one field is specified

        # Read the entire request body as a JSON
        # This will fail if the request body is NOT a JSON.
        input_json = request.json

        Brevet.objects.get(id=_id).update(**input_json)
        return f"Updated the record with id: {_id}", 200

    def delete(self, _id):
        # Should delete brevet with the id: _id
        Brevet.objects(id=_id).delete() # does not return anything

        return f"Deleted the record with id: {_id}", 200
