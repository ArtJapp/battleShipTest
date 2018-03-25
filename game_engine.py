from settings import *
import random
from player import Player

#todo check function that checks the end of game
class Game:
    def __init__(self, game_id, player1):
        self.id = game_id
        self.field = []
        self.players = [Player(player1, 0)]
        self.running = False
        self.finished = False
        self.error = False
    #    self.pointer = 0   in case of do more logic on the backend
        self.createfield()
        self.current_player = 0

        self.winner = -1

    def createfield(self):
        '''
        здесь создается матрица размером [FIELD_SIZE_X][FIELD_SIZE_Y], хранящая в себе лист из 4 элементов:
        - сделал ли 1 игрок сюда ход
        - установил ли 1 игрок сюда свой корабль
        - сделал ли 2 игрок сюда ход
        - установил ли 2 игрок сюда корабль
        :return:
        '''
        self.field = [[['0'] * 4 for j in range(FIELD_SIZE_Y)] for i in range(FIELD_SIZE_X)]

    def join_user2(self, player2):
        if len(self.players) >= 2:
            return False
        self.players.append(Player(player2, 1))
        return True

    def ustanovka(self, **kwargs):
        player = kwargs['user_id']
        self.players[player].set_ships(kwargs['ships'])

    def printfield(self):
        for x in range(0, FIELD_SIZE_X):
            for y in range(0, FIELD_SIZE_Y):
                print("".join(self.field[x][y]), end=" ")
            print()

    def fire(self, coor_x, coor_y, player):
        print("Player ", player, " hits in cell (", coor_x+1, ", ", coor_y+1, ")", end="   ")
        hited = False
        killed = False
        if player == self.current_player:

            enemy = (player + 1) % 2
            gamer = self.players[enemy]

            hited, killed = gamer.fire(coord_x=coor_x, coord_y=coor_y)

            if hited:
                print("HIT")
                self.current_player = player
            else:
                print("MISS")
                self.current_player = enemy

            if killed:
                print("Ship is killed")
        else:
            print("Not your hod, bitch")
            self.error = True
        return hited, killed, self.get_error()

    def get_error(self):
        ans = self.error
        self.error = False
        return ans


    def checker(self):
        ans1 = False
        ans2 = False

        ans1 = self.players[0].still_alive()
        ans2 = self.players[1].still_alive()

        if ans1 and not ans2:
            self.finished = True
            self.winner = 0
        if ans2 and not ans1:
            self.finished = True
            self.winner = 1

    def statistics(self):
        self.checker()

        return {
            "game_id": self.id,
            "winner_id": self.winner,
            "users": [
                {
                    "user_id": 0,
                    "hits": self.players[0].get_hits(),
                    "fires": self.players[0].get_fires(),
                   # "area": [[y[1] for y in x] for x in self.field]
                },
                {
                    "user_id": 1,
                    "hits": self.players[1].get_hits(),
                    "fires": self.players[1].get_fires(),
                   # "area": [[y[3] for y in x] for x in self.field]
                },
            ],
        }

