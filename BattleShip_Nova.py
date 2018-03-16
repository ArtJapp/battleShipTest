from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, close_room, leave_room, emit
from game_engine import *
from player import *

app = Flask(__name__)
socketio = SocketIO(app)

ROOMS = {}

@app.route('/')
def hello_world():
    return render_template("index.html")


@socketio.on('create')
def start_game(data):
    print(data['name'])
    game_id = len(ROOMS)
    ROOMS[game_id] = Game(game_id, data['name'])
    print("The game with id=", game_id, " has been created")
    join_room(game_id)
    emit('created', {'game_id': game_id, 'user_id': 0})
    

@socketio.on('join')
def start_game(data):
    game_id = int(data['game_id'])
    if len(ROOMS) > game_id:
        game = ROOMS[game_id]
        answer = game.join_user2(data['name'])
        if answer:
            print("Yes, gamer ", data['name'], " has joined")
            join_room(game_id)
            emit('joined', {
                'game_id': game.id,
                'user': {
                    'id': game.players[0].get_id(),
                    'name': game.players[0].get_name()
                },
                'enemy': {
                    'id': game.players[1].get_id(),
                    'name': game.players[1].get_name()
                }
            })
        else:
            print("Nope, gamer ", data['name'], " cannot join this game")
            some_users_list = []
            for x in game.players:
                some_users_list.append(x.get_name())
            emit('forbidden', {
                'game_id': game.id,
                'users_id': some_users_list
            })
    else:
        print("The game with id=", game_id, " doesn't exist")


if __name__ == '__main__':
    socketio.run(app, port=5010)
