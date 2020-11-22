from app import app
from flask import render_template, jsonify, session
from app.repositories import GameRepository
import uuid



@app.route('/')
@app.route('/index')
def index():
    if 'id' not in session:
        session['id'] = uuid.uuid4()
        session['username'] = 'ben'

    return render_template('base.html')

@app.route('/api/games/', methods=['post'])
def create_game():
    print(session)
    game = GameRepository.create()
    return jsonify(game.as_dict())

@app.route('/api/games/:id', methods=['get'])
def fetch_game(id):
    game = GameRepository.get(id)
    return jsonify(game.as_dict())


@app.route('/api/games/:id/start', methods=['post'])
def start_game(id):
    game = GameRepository.get(id)
    game.start()
    return jsonify(game.as_dict())


@app.route('/api/games/:id/move', methods=['post'])
def play_move(id):
    game = GameRepository.get(id)
    game.move()
    return jsonify(game.as_dict())


