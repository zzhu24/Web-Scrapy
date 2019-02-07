from urllib.request import urlopen
from bs4 import BeautifulSoup
from operator import itemgetter
from src import *
import logging
import time
import json
import ast
import re
import flask
from flask import Flask, request, jsonify
import api
import os
import requests

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return flask.make_response(jsonify({'error': 'Not found'}), 404)


"""
Actors GET
"""


#http://127.0.0.1:5000/actors/Tom
@app.route('/actors/<string:attribute>', methods=['GET'])
def simple_get_actor(attribute):
    for actor in data["Stars"]:
        if attribute in actor["Actor Name"]:
            return jsonify({'Actors': actor})
    return flask.make_response(jsonify({'error': 'Not found: ' + attribute}), 404)

#http://127.0.0.1:5000/actors?name=Tom&age=1996
#http://127.0.0.1:5000/actors?name=Jenny&age=1982
#http://127.0.0.1:5000/actors?name1=Tom&name2=Michael
#http://127.0.0.1:5000/actors?name1=Tom&name2=Matt
@app.route('/actors', methods=['GET'])
def get_actor_boolean():
    name = request.args.get('name')
    age = request.args.get('age')
    name1 = request.args.get('name1')
    name2 = request.args.get('name2')
    all_actor = []
    if name is not None and age is not None:
        for actor in data["Stars"]:
            if name in actor["Actor Name"] and str(age) in actor["Actor Birthday"]:
                all_actor.append(actor)
    if name1 is not None and name2 is not None:
        for actor in data["Stars"]:
            if name1 in actor["Actor Name"]:
                all_actor.append(actor)
            if name2 in actor["Actor Name"]:
                all_actor.append(actor)
    if len(all_actor) == 0:
        return flask.make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify({'Actors': all_actor})




"""
Films GET
"""


#http://127.0.0.1:5000/movies/The Impossible (2012 film)
@app.route('/movies/<string:attribute>', methods=['GET'])
def simple_get_movie(attribute):
    for movie in data["Movies"]:
        if attribute in movie["Movie Name"]:
            return jsonify({'Movies': movie})
    return flask.make_response(jsonify({'error': 'Not found: ' + attribute}), 404)

#http://127.0.0.1:5000/movies?name=Not&year=2001
#http://127.0.0.1:5000/movies?name1=of&name2=The
@app.route('/movies', methods=['GET'])
def get_movie_boolean():
    name = request.args.get('name')
    year = request.args.get('year')
    name1 = request.args.get('name1')
    name2 = request.args.get('name2')
    all_movie = []
    if name is not None and year is not None:
        for movie in data["Movies"]:
            if name in movie["Movie Name"] and str(year) in str(movie["Movie Year"]):
                all_movie.append(movie)
    if name1 is not None and name2 is not None:
        for movie in data["Movies"]:
            if name1 in movie["Movie Name"] and name2 in movie["Movie Name"]:
                all_movie.append(movie)

    if len(all_movie) == 0:
        return flask.make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify({'Movies': all_movie})


"""
Actors PUT
"""

#http://127.0.0.1:5000/actors/update/Matt McCoy
#{"Actor Total Gross":204080}
@app.route('/actors/update/<string:attribute>', methods=['PUT'])
def update_actor(attribute):
    temp_actor = None
    for actor in data["Stars"]:
        if attribute in actor["Actor Name"]:
            temp_actor = actor
    if temp_actor is None:
        return flask.make_response(jsonify({'error': 'Actor Not found'}), 404)

    new_actor = request.get_json()
    for key in new_actor:
        try:
            temp_actor[key] = new_actor[key]
        except:
            return flask.make_response(jsonify({'error': 'Key Not Found'}), 404)
    # load new information to json file
    with open("temp_data.json", 'w') as f:
        json.dump(data, f, indent=4)

    return jsonify({"result": 'Info has been updated ~ ~'}, 201)



"""
Movie PUT
"""

#http://127.0.0.1:5000/movies/update/Impossible
#{"Movie Box Office":204080}
@app.route('/movies/update/<string:attribute>', methods=['PUT'])
def update_movie(attribute):
    temp_movie = None
    for movie in data["Movies"]:
        if attribute in movie["Movie Name"]:
            temp_movie = movie
    if temp_movie is None:
        return flask.make_response(jsonify({'error': 'Movie Not found'}), 404)

    new_temp_movie = request.get_json()
    for key in new_temp_movie:
        try:
            temp_movie[key] = new_temp_movie[key]
        except:
            return flask.make_response(jsonify({'error': 'Key Not Found'}), 404)
    # load new information to json file
    with open("temp_data.json", 'w') as f:
        json.dump(data, f, indent=4)

    return jsonify({"result": 'Info has been updated ~ ~'}, 201)



"""
Actor POST
"""
#http://127.0.0.1:5000/actors/add/Kamiya
"""
{
    "result": {
        "Actor Birthday": "1975-01-28",
        "Actor Filmography": [
            "Attack on Titan",
            "Shirokuma Cafe"
        ],
        "Actor Name": "Kamiya",
        "Actor Total Gross": 900000,
        "Actor URL": "https://en.wikipedia.org/wiki/Hiroshi_Kamiya"
    }
}
"""
@app.route('/actors/add/<string:attribute>', methods=['POST'])
def add_actor(attribute):
    for actor in data["Stars"]:
        if attribute == actor["Actor Name"]:
            return flask.make_response(jsonify({'error': 'INFO Already Exists ~ ~'}), 404)
    new_actor = request.get_json()
    data["Stars"].append(new_actor)
    with open("temp_data.json", 'w') as f:
        json.dump(data, f, indent=4)
    return jsonify({'result': new_actor}), 201

"""
Movie POST
"""
#http://127.0.0.1:5000/movies/add/Howl
"""
        {
            "Movie Name": "Howl's Moving Castle",
            "Moive URL": "https://en.wikipedia.org/wiki/Howl%27s_Moving_Castle_(film)",
            "Movie Year": 2004,
            "Movie Box Office": 24000000,
            "Movie Casting": [
                "Chieko Baisho",
                "Takuya Kimura",
                "Akihiro Miwa"
            ]
        }

"""

@app.route('/movies/add/<string:attribute>', methods=['POST'])
def add_movie(attribute):
    for movie in data["Movies"]:
        if attribute == movie["Movie Name"]:
            return flask.make_response(jsonify({'error': 'INFO Already Exists ~ ~'}), 404)
    new_movie = request.get_json()
    data["Movies"].append(new_movie)
    # load new information to json file
    with open("temp_data.json", 'w') as f:
        json.dump(data, f, indent=4)
    return jsonify({'result': new_movie}), 201




"""
Actor DELETE
"""
#http://127.0.0.1:5000/actors/delete/Kamiya
@app.route('/actors/delete/<string:attribute>', methods=['DELETE'])
def delete_actor(attribute):
    temp_actor = None
    for i in range(len(data["Stars"])):
        if attribute in data["Stars"][i]["Actor Name"]:
            temp_actor = data["Stars"][i]
            del data["Stars"][i]
    if temp_actor is None:
        flask.make_response(jsonify({'error': 'Actor Is Not Found ~ ~'}), 404)


    with open("temp_data.json", 'w') as f:
        json.dump(data, f, indent=4)
    return jsonify({'result':"Deleted successfully ~ ~"}), 201


"""
Movie DELETE
"""
#http://127.0.0.1:5000/movies/delete/Howl's Moving Castle
@app.route('/movies/delete/<string:attribute>', methods=['DELETE'])
def delete_movie(attribute):
    temp_movie = None
    for i in range(len(data["Movies"])):
        if attribute == data["Movies"][i]["Movie Name"]:
            temp_movie = data["Movies"][i]
            del data["Movies"][i]
    if temp_movie is None:
        flask.make_response(jsonify({'error': 'Movie Is Not Found ~ ~'}), 404)


    with open("temp_data.json", 'w') as f:
        json.dump(data, f, indent=4)
    return jsonify({'result':"Deleted successfully ~ ~"}), 201







if __name__ == "__main__":
    json_data = open("temp_data.json").read()
    data = json.loads(json_data)

    app.run(debug=True)