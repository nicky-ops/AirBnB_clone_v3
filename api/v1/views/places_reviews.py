#!/usr/bin/python3
"""
creating a view for Review objects
"""
from api.v1.views import app_views
from flask import jsonify, Flask, abort, request
from models import storage
from models.review import Review
from models.place import Place


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews(place_id):
    '''RETRIEVE THE LIST OF ALL review OBJECTS'''
    place = storage.get(Place, place_id)
    if place:
        places_lst = [obj.to_dict() for obj in place.reviews]
    else:
        abort(404)
    return jsonify(places_lst)


@app_views.route('/reviews/<string:review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    '''retrive a review object by its id'''
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    '''delete a review object'''
    review = storage.get(Review, review_id)
    if review:
        review.delete()
    else:
        abort(404)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    '''create a review object'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'text' not in request.get_json():
        abort(400, 'Missing text')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    state_data = request.get_json()
    user = storage.get(User, state_data['user_id'])
    if not user:
        abort(404)
    review = Review(**state_data)
    review.place_id = place.id
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    '''update a review by its id'''
    review = storage.get(Review, review_id)
    data = request.get_json()
    if not request.get_json():
        abort(400, 'Not a JSON')
    if review:
        for key, value in data.items():
            if key not in ['id', 'user_id', 'place_id',
                           'created_at', 'updated_at']:
                setattr(review, key, value)
    else:
        abort(404)
    storage.save()
    return jsonify(review.to_dict()), 200
