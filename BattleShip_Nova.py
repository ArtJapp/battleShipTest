from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, close_room, leave_room, emit
from game_engine import *
from player import *

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins=["http://alexfilimon.ru", "https://heroku.com"])

ROOMS = {}

@app.route('/')
def hello_world():
    return render_template("index.html")


@socketio.on('connect')
def connected_init():
    print("somebody has connected")
    emit('connected', {'dorou': "there"})
 #   print(request.sid)


@socketio.on('create')
def create_game(data):
    print(data['name'])
    game_id = len(ROOMS)
    ROOMS[game_id] = Game(game_id, data['name'])
    print("The game with id=", game_id, " has been created")
    join_room(game_id)
    emit('created', {'game_id': game_id, 'user_id': 0, 'user_name': data['name']})
    

@socketio.on('join')
def join_game(data):
    # TODO change condition (if len(ROOMS) > game_id) with try/except
    game_id = int(data['game_id'])
    if len(ROOMS) > game_id:
        game = ROOMS[game_id]
        answer = game.join_user2(data['name'])
        if answer:
            print("Yes, gamer ", data['name'], " has joined")
            join_room(game_id)

            emit('joined', {
                'game_id': game.id,
                'enemy': {
                    'id': game.players[0].get_id(),
                    'name': game.players[0].get_name()
                },
                'user': {
                    'id': game.players[1].get_id(),
                    'name': game.players[1].get_name()
                }
            }, room=game_id)
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


@socketio.on("setup-ships")
def setting_ships_up(data):
    game_id = int(data['game_id'])
    player_id = int(data['user_id'])
   # print("Ships has been planted", data)
    ships = data['ships']

    try:
        game = ROOMS[game_id]
        for x in ships:
            size = x['size']
            coordinates = x['coordinates']
            print(size)
            for m in coordinates:
                print(m)
                x = m['x']
                y = m['y']
                game.ustanovka(coor_x=x, coor_y=y, player=player_id)
        if player_id == 0:
            game.setted_1 = True
        elif player_id == 1:
            game.setted_2 = True
        if game.setted_1 and game.setted_2:
            print("The game id=", game_id, " starts")
            game.running = True
            socketio.emit("game-started", {
                "game_id": game_id,
                "next_player_id": 0
            })

    except KeyError:
        print("No game with such id")
        emit('error', {
            'message': "No game with such ID"
        })


@socketio.on("fire")
def player_fire(data):
    game_id = int(data['game_id'])
    user_id = int(data['user_id'])
    # if user_id == 1, then enemy_id == (1+1)%2 == 0
    enemy_id = (user_id + 1)%2
    print(data)
    coord_x = int(data['coord']['x'])
    coord_y = int(data['coord']['y'])
    print(coord_x, coord_y)
    try:
        game = ROOMS[game_id]
        answer = game.fire(coord_x, coord_y, user_id)
        if answer:
            next_player_id = user_id
        else:
            next_player_id = enemy_id

        if game.finished:
            print("the game is finished")
            emit("fired", {
                'game_id': game_id,
                'enemy_id': enemy_id,
                'next_player_id': -1,
                'is_ship': answer,
                'coord': {
                    'x': coord_x,
                    'y': coord_y
                }
            }, room=game_id)
        emit("fired", {
            'game_id': game_id,
            'enemy_id': enemy_id,
            'next_player_id': next_player_id,
            'is_ship': answer,
            'coord': {
                'x': coord_x,
                'y': coord_y
            }
        }, room=game_id)
    except KeyError:
        emit('error', {
            'message': "kind of turururu"
        })


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5010)
