from settings import *
import random
from player import *

#todo check function that checks the end of game
class Game:
    def __init__(self, game_id, player1):
        self.id = game_id
        self.field = []
        self.players = [Player(player1, 0)]
        self.running = False
        self.setted_1 = False
        self.setted_2 = False
        self.finished = False
        self.error = False
    #    self.pointer = 0   in case of do more logic on the backend
        self.createfield()
        self.current_player = 0
        self.popadeniya1 = 0
        self.popadeniya2 = 0

        self._ship_killed = False

        self.fires1 = 0
        self.fires2 = 0
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

    def ustanovka(self, coor_x, coor_y, player):
        player += 1
        if player == 1:
            self.field[coor_y][coor_x][1] = '1'
        elif player == 2:
            self.field[coor_y][coor_x][3] = '1'

    def printfield(self):
        for x in range(0, FIELD_SIZE_X):
            for y in range(0, FIELD_SIZE_Y):
                print("".join(self.field[x][y]), end=" ")
            print()

    def fire(self, coor_x, coor_y, player):
        print("Player ", player, " hits in cell (", coor_x+1, ", ", coor_y+1, ")", end="   ")
        if player == 0:
            #проверка кораблей второго игрока

            if self.field[coor_y][coor_x][3] == '1':
                if self.field[coor_y][coor_x][0] == '0':
                    self.field[coor_y][coor_x][0] = '1'

                    self.popadeniya1 += 1
                    self.fires1 += 1
                    self._ship_killed = self.killed_ship(coor_x, coor_y, player)

                    print("HIT")
                    self.checker()
                else:
                    # если пользователь уже бил в это поле
                    self.error = True
                return True
            else:
                if self.field[coor_y][coor_x][0] == '0':
                    self.field[coor_y][coor_x][0] = '1'

                    self.fires1 += 1

                    print("MISS")
                    self.checker()
                else:
                    self.error = True
                return False
        else:
            if self.field[coor_y][coor_x][1] == '1':
                if self.field[coor_y][coor_x][2] == '0':
                    self.field[coor_y][coor_x][2] = '1'

                    self.popadeniya2 += 1
                    self.fires2 += 1
                    self._ship_killed = self.killed_ship(coor_x, coor_y, player)

                    print("HIT")
                    self.checker()
                else:
                    self.error = True
                return True
            else:
                if self.field[coor_y][coor_x][2] == '0':
                    self.field[coor_y][coor_x][2] = '1'

                    self.fires2 += 1

                    print("MISS")
                    self.checker()
                else:
                    self.error = True
                return False

    def join_user2(self, player2):
        if len(self.players) >= 2:
            return False
        self.players.append(Player(player2, 1))
        return True

    def killed_ship(self, coord_x, coord_y, player):
        if player == 0:
            positition_move = 0
            positition_fire = 3
        else:
            positition_move = 2
            positition_fire = 1
        ans = True
        for y in range(coord_y-1, coord_y+2):
            if y >= 0:
                print(y, ":   ", end="")
                for x in range(coord_x-1, coord_x+2):
                    if x >= 0:
                        if self.field[y][x][positition_fire] == '1' and self.field[y][x][positition_move] == '0':
                            ans = False
                print()

        if ans:
            print("the ship is killed")
        return ans

    def get_killed_ship(self):
        ans = self._ship_killed
        self._ship_killed = False
        return ans

    def checker(self):
        ans1 = False
        ans2 = False
        for y in self.field:
            for x in y:
                if ans1 and ans2:
                    #it means that both sides have at least 1 cell alive
                    self.finished = False
                    return
                if x[1] == '1' and x[2] == '0':
                    #the gamer 1 has not bitten cell
                    ans2 = True
                if x[0] == '0' and x[3] == '1':
                    #the gamer 2 has not bitten cell
                    ans1 = True
        if ans1 and not ans2:
            self.finished = True
            self.winner = 1
        if ans2 and not ans1:
            self.finished = True
            self.winner = 0

    def statistics(self):
        self.checker()
        return {
            "game_id": self.id,
            "winner_id": self.winner,
            "gamer_1": {
                "hits": self.popadeniya1,
                "fires": self.fires1
            },
            "gamer_2": {
                "hits": self.popadeniya2,
                "fires": self.fires2
            }
        }

