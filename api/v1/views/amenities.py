#!/usr/bin/python3
""" a view for Amenity objects that handles
all default RestFul API actions for Amenities"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """
    Retrieves a list of all amenities objects
    """
    allAmenities = storage.all(Amenity).values()
    amenities_list = []
    for amenity in allAmenities:
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>/', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves a specific amenity """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes an amenity  Object
    """

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Creates a new amenity object
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Amenity(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates an amenity object
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
