"""Star Wars Character Maps"""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

import requests

import json

app = Flask(__name__)

app.secret_key = "oisjdfonero87aw9ed8afsond"

app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage"""

    character_info = {}

    p = requests.get('http://swapi.co/api/people/')
    people = p.json()

    results = people['results']

    for person in results:
        name = person['name']
        movies = person['films']
        films = []
        for movie in movies:
            m = requests.get(movie)
            movie_json = m.json()
            title = movie_json['title']
            films.append(title)
        character_info[name] = films


    return render_template("homepage.html",
                            character_info=character_info)




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    # connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')