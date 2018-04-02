from game_engine import Game
import json

ERRORS = {
    "505": {
        # player didn't send his decision on the time
        "message": "TimeOut"
    },
    "519": {
        # user tries to join not existing game
        "message": "NoGame"
    },
    "520": {
        #    user tries to join already started game
        #    as a third player
        "message": "Forbidden"
    },
    "521": {
        #    player tries to fire already fired cell
        "message": "Pushed"
    },
    "522": {
        #    player tries to fire when the game is not
        #    started or has been already finished
        "message": "NotActive"
    },
    "219": {
        #    created new game
        "message": "Created"
    },
    "221": {
        #    second player joined
        "message": "Joined"
    },
    "223": {
        #    both players set ships up, the game starts
        "message": "Started"
    },
    "225": {
        #    player fired a cell with no enemy ship
        "message": "FiredMiss"
    },
    "227": {
        #    player tries to fire when the game is not
        #    started or has been already finished
        "message": "FiredHit"
    },
    "231": {
        #    player tries to fire when the game is not
        #    started or has been already finished
        "message": "ChatSent"
    },
    "233": {
        #    player tries to fire when the game is not
        #    started or has been already finished
        "message": "ChatWasRead"
    },
    "235": {
        #    player tries to fire when the game is not
        #    started or has been already finished
        "message": "ChatTyping"
    },
    "245": {
        #    player tries to fire when the game is not
        #    started or has been already finished
        "message": "AreYouHere"
    },
    "249": {
        #
        "message": "LazyStatistics"
    },
    "250": {
        #    player tries to fire when the game is not
        #    started or has been already finished
        "message": "Disconnected"
    },
}


class Signals:
    def __init__(self, code, **kwargs):
        self.code = code
        self.header = ERRORS[str(code)]["message"]

        if code == 505:
            game = kwargs['game']
            self.message = "Time is over"
        elif code == 519:
            self.message = "No game with such ID"
            self.id = int(kwargs['id'])
            print(self.id)
        elif code == 520:
            self.message = "Sorry, this game already has 2 players"
            game = kwargs['game']
            self.game_id = game.id
            self.users_id = [x.get_id() for x in game.players]
            self.gamers = [x.get_name() for x in game.players]
        elif code == 521:
            game = kwargs['game']
            self.game_id = game.id
            self.message = "Player has already fired here!"
        elif code == 522:
            game = kwargs['game']
            self.game_id = game.id
            self.finished = game.finished
            if self.finished:
                self.message = "This game has been already finished"
                self.winner = game.winner
            else:
                self.message = "This game has been never started"
        elif code == 219:
            game = kwargs['game']
            name = kwargs['name']
            self.game_id = game.id
            self.user_id = 0
            self.user_name = name
        elif code == 221:
            game = kwargs['game']
            self.game_id = game.id
            self.enemy = {
                'id': game.players[0].get_id(),

                'name': game.players[0].get_name()
            }
            self.user = {
                'id': game.players[1].get_id(),
                'name': str(game.players[1].get_name())
            }
        elif code == 223:
            game = kwargs['game']
            self.game_id = game.id
            self.next_player_id = 0

        elif code == 249:
            game = kwargs['game']
            alive_id = kwargs['id']
            self.game_id = game.id
            self.winner_id = game.winner
            self.user = {
                    "user_id": alive_id,
                    "hits": game.players[alive_id].get_hits(),
                    "fires": game.players[alive_id].get_fires(),
                    "ships": game.players[alive_id].get_ships()
                }

            self.enemy_ship = game.players[(alive_id + 1) % 2].get_ships()

    def __str__(self):
        attres = vars(self)
        return attres

