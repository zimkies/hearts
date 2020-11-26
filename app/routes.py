from app import app
from flask import render_template, jsonify, session
from app.repositories import GameRepository
import uuid



@app.route('/')
@app.route('/index')
@app.route('/games/<id>')
def index(id=None):
    if 'id' not in session:
        session['id'] = uuid.uuid4().hex[:5]
        session['username'] = 'ben'

    return render_template('base.html')

@app.route('/api/games/', methods=['post'])
def create_game():
    print(session)
    game = GameRepository.create()
    game.add_player(player=session['id'], position=0)

    return jsonify(game.as_dict_for_player(session['id']))

@app.route('/api/games/<game_id>', methods=['get'])
def fetch_game(game_id):
    game = GameRepository.get(game_id)
    return jsonify(game.as_dict_for_player(session['id']))


@app.route('/api/games/<game_id>/start', methods=['post'])
def start_game(game_id):
    game = GameRepository.get(game_id)

    game.start()

    return jsonify(game.as_dict_for_player(session['id']))


@app.route('/api/games/<game_id>/move', methods=['post'])
def game_move(game_id):
    game = GameRepository.get(game_id)

    game.move(session['id'], card)


    return jsonify(game.as_dict_for_player(session['id']))
