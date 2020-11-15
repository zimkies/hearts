from app import app
from flask import render_template, jsonify
from collections import namedtuple


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')


Game = namedtuple('Game', ["id"])

@app.route('/api/games/', methods=['post'])
def create_game():
    game = Game(id='chicken')
    return jsonify(game._asdict())
