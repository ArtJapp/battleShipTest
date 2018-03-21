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
    }
}


class Signals:
    def __init__(self, code, **kwargs):
        self.code = code
        self.header = ERRORS[str(code)]["message"]

        if code == 519:
            self.message = "No game with such ID"
        elif code == 520:
            self.game_id = kwargs['game'].id
            self.users_id = [x.get_id() for x in kwargs['game'].players]
            self.gamers = [x.get_name() for x in kwargs['game'].players]
        elif code == 521:
            self.game_id = kwargs['game'].id
            self.message = "Player has already fired here!"
        elif code == 522:
            game = kwargs['game']
            self.game_id = game.id
            self.finished = game.finished
            if self.finished:
                self.winner = game.winner

    def __str__(self):
        attres = vars(self)
        return str(attres)


gam = Game(4, "pushok")
gam.join_user2("not pushok")
sgn = Signals(520, game=gam)
attrs = vars(sgn)
print(attrs)
print(str(sgn))
