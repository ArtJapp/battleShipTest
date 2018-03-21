from game_engine import Game

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
        "message": "NotActive"
    },
    "231": {
        #    player tries to fire when the game is not
        #    started or has been already finished
        "message": "NotActive"
    },
    "233": {
        #    player tries to fire when the game is not
        #    started or has been already finished
        "message": "NotActive"
    },
    "235": {
        #    player tries to fire when the game is not
        #    started or has been already finished
        "message": "NotActive"
    },
    "245": {
        #    player tries to fire when the game is not
        #    started or has been already finished
        "message": "NotActive"
    },
    "250": {
        #    player tries to fire when the game is not
        #    started or has been already finished
        "message": "NotActive"
    },
}


class Signals:
    def __init__(self, code, **kwargs):
        self.code = code
        self.header = ERRORS[str(code)]["message"]
        game = kwargs['game']

        if code == 505:
            self.message = "Time is over"
        elif code == 519:
            self.message = "No game with such ID"
        elif code == 520:
            self.game_id = game.id
            self.users_id = [x.get_id() for x in game.players]
            self.gamers = [x.get_name() for x in game.players]
        elif code == 521:
            self.game_id = game.id
            self.message = "Player has already fired here!"
        elif code == 522:
            self.game_id = game.id
            self.finished = game.finished
            if self.finished:
                self.winner = game.winner
        elif code == 221:
            self.game_id = game.id
            self.enemy = {
                'id': game.players[0].get_id(),
                'name': game.players[0].get_name()
            }
            self.user = {
                'id': game.players[1].get_id(),
                'name': game.players[1].get_name()
            }


    def __str__(self):
        attres = vars(self)
        return str(attres)


gam = Game(4, "pushok")
gam.join_user2("not pushok")
sgn = Signals(221, game=gam)
print(str(sgn))
