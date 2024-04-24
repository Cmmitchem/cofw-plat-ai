from flask import Blueprint, request, jsonify
from db import get_movie, get_movies

from flask_cors import CORS
from utils import expect
from datetime import datetime


#movies_api_v1 = Blueprint(
#    'movies_api_v1', 'movies_api_v1', url_prefix='/api/v1/movies')
movies_api_v1 = Blueprint('movies_api_v1', __name__)

CORS(movies_api_v1)

@movies_api_v1.route('http://127.0.0.1:5000/all_movies', methods=['GET'])
def api_get_movies():
    MOVIES_PER_PAGE = 20

    (movies, total_num_entries) = get_movies(
        None, page=0, movies_per_page=MOVIES_PER_PAGE)

    response = {
        "movies": movies,
        "page": 0,
        "filters": {},
        "entries_per_page": MOVIES_PER_PAGE,
        "total_results": total_num_entries,
    }
    return("flask api is working")
    #return jsonify(response)

@movies_api_v1.route('/id/<id>', methods=['GET'])
def api_get_movie_by_id(id):
    movie = get_movie(id)
    if movie is None:
        return jsonify({
            "error": "Not found"
        }), 400
    elif movie == {}:
        return jsonify({
            "error": "uncaught general exception"
        }), 400
    else:
        updated_type = str(type(movie.get('lastupdated')))
        return jsonify(
            {
                "movie": movie,
                "updated_type": updated_type
            }
        ), 200