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

    def computer_initial(self, player=1):
        if player == 0:
            position = 1
        else:
            position = 3
        for i in range(1, MAX_LENGTH_SHIP+1):
            print(MAX_LENGTH_SHIP+2-i)
            for j in range(0, MAX_LENGTH_SHIP+1-i):
                cur_size = i
                rand_vorh = random.randint(0, 100) % 2
                if rand_vorh:
                    #horyzontal
                    coord_x = random.randint(1, FIELD_SIZE_X-cur_size) - 1
                    coord_y = random.randint(1, FIELD_SIZE_Y) - 1
                    while self.field[coord_x][coord_y][position] == '1':
                        coord_x = random.randint(1, FIELD_SIZE_X - cur_size) - 1
                        coord_y = random.randint(1, FIELD_SIZE_Y) - 1
                    print("horyz: ", coord_x, coord_y)
                else:
                    coord_x = random.randint(1, FIELD_SIZE_X) - 1
                    coord_y = random.randint(1, FIELD_SIZE_Y - cur_size) - 1
                    while self.field[coord_x][coord_y][position] == '1':
                        coord_x = random.randint(1, FIELD_SIZE_X) - 1
                        coord_y = random.randint(1, FIELD_SIZE_Y - cur_size) - 1
                    print("vert: ", coord_x, coord_y)
                  #  self.ustanovka(coord_x, coord_y, cur_size, 'v', position+1)

    def computer_gamer(self):
        choosen_x = random.randint(1, FIELD_SIZE_X) - 1
        choosen_y = random.randint(1, FIELD_SIZE_Y) - 1
        while self.field[choosen_x][choosen_y][2] != '0':
            choosen_x = random.randint(1, FIELD_SIZE_X) - 1
            choosen_y = random.randint(1, FIELD_SIZE_Y) - 1
        self.fire(choosen_x, choosen_y, 2)

    def user_gamer(self, player):
        choosen_x = int(input("Выберите координату х"))-1
        choosen_y = int(input("Выберите координату y"))-1

        if player == 0:
            position = 1
        else:
            position = 3
        if 0 <= choosen_y < FIELD_SIZE_Y and FIELD_SIZE_X > choosen_x >= 0:
            return self.fire(choosen_x, choosen_y, position)

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
            print(self.winner, self.players[self.winner])
        if ans2 and not ans1:
            self.finished = True
            print(self.winner, self.players[self.winner])
            self.winner = 0

    def auto_ustanovka_testers(self):
        self.computer_initial(0)
        self.computer_initial(1)
        self.printfield()

    def statistics(self):
        return {
            "game_id": self.id,
            "winner": self.winner,
            "gamer_1": {
                "hits": self.popadeniya1,
                "fires": self.fires1
            },
            "gamer_2": {
                "hits": self.popadeniya2,
                "fires": self.fires1
            }
        }

