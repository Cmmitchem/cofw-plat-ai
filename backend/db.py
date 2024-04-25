"""
This module contains all database interfacing methods for the MFlix
application. You will be working on this file for the majority of M220P.

Each method has a short description, and the methods you must implement have
docstrings with a short explanation of the task.

Look out for TODO markers for additional help. Good luck!
"""
import bson

from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:

        db = g._database = PyMongo(current_app).db
       
    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)

def get_movie(id):
    """
    Given a movie ID, return a movie with that ID, with the comments for that
    movie embedded in the movie document. The comments are joined from the
    comments collection using expressive $lookup.
    """
    try:

        pipeline = [
            {
                "$match": {
                    "_id": ObjectId(id)
                }
            }
        ]

        movie = db.movies.aggregate(pipeline).next()
        return movie

    # TODO: Error Handling
    # If an invalid ID is passed to `get_movie`, it should return None.
    except (StopIteration) as _:

        return None

    except Exception as e:
        return {}

def build_query_sort_project(filters):
    """
    Builds the `query` predicate, `sort` and `projection` attributes for a given
    filters dictionary.
    """
    query = {}
    # The field "tomatoes.viewer.numReviews" only exists in the movies we want
    # to display on the front page of MFlix, because they are famous or
    # aesthetically pleasing. When we sort on it, the movies containing this
    # field will be displayed at the top of the page.
    sort = [("tomatoes.viewer.numReviews", -1)]
    project = None
    if filters:
        if "text" in filters:
            query = {"$text": {"$search": filters["text"]}}
            meta_score = {"$meta": "textScore"}
            sort = [("score", meta_score)]
            project = {"score": meta_score}
        elif "cast" in filters:
            query = {"cast": {"$in": filters["cast"]}}
        elif "genres" in filters:

            """
            Ticket: Text and Subfield Search

            Given a genre in the "filters" object, construct a query that
            searches MongoDB for movies with that genre.
            """

            # TODO: Text and Subfield Search
            # Construct a query that will search for the chosen genre.
            query = {}

    return query, sort, project

def get_movies(filters, page, movies_per_page):
    """
    Returns a cursor to a list of movie documents.

    Based on the page number and the number of movies per page, the result may
    be skipped and limited.

    The `filters` from the API are passed to the `build_query_sort_project`
    method, which constructs a query, sort, and projection, and then that query
    is executed by this method (`get_movies`).

    Returns 2 elements in a tuple: (movies, total_num_movies)
    """
    query, sort, project = build_query_sort_project(filters)
    if project:
        cursor = db.movies.find(query, project).sort(sort)
    else:
        cursor = db.movies.find(query).sort(sort)

    total_num_movies = 0
    if page == 0:
        total_num_movies = db.movies.count_documents(query)
 
    movies = cursor.limit(movies_per_page)

    return (list(movies), total_num_movies)

def get_plats(page, items_per_page):
    collection = db["city_of_fort_worth_vector_collection"]
    #plats = db.city_of_fort_worth_vector_collection.find_one()
    
    # Calculate the number of documents to skip
    #skips = items_per_page * (page - 1)
    # Use find() to retrieve documents with pagination
    plats = list(collection.find().limit(items_per_page))
    
    return (plats)

