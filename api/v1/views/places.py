#!/usr/bin/python3
"""a view objects that handle all default RestFul API actions for Places """

from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City
    """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    places = [place.to_dict() for place in city.places]

    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a specific Place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place Object
    """

    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a new Place object
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    data = request.get_json()
    user = storage.get(User, data['user_id'])

    if not user:
        abort(404)

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data["city_id"] = city_id
    instance = Place(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object 
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)

@app_views.route('/places_search', method=['POST'], strict_slashes=False)
def places_search():
    """
    retrieves all Place obj depending on the JSON in the body of the request
    """
    if not request.json:
        abort(400, "Not a JSON")

    states = request.json.get('state', [])
    cities = request.json.get('cities', [])
    amenities = request.json.get('amenities', [])

    if not states and not cities and not amenities:
        places = storage.all(Place).values()
        return jsonify([places.to_dict() for place in places)

    places = set()

    # add all places from the state
    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            for city in state.cities:
                places.update(city.places)

    # Add places from cities
    for city_id in cities:
        city = storage.get(City, city_id)
        if city:
            places.update(city.places)

    # Filter places by amenities
    if amenities:
        amenities_set = set(amenities)
        places = [place for place in places if amenities_set.issubset(place.amenity_ids)]

    return jsonify([place.to_dict() for place in places])
