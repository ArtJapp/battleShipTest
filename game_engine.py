from settings import *
import random
from player import *


class Game:
    def __init__(self, game_id, player1):
        self.id = game_id
        self.field = []
        self.players = [Player(player1, 0)]
        self.running = False
        self.finished = False
        self.createfield()
        self.popadeniya1 = 0
        self.popadeniya2 = 0
        self.maxpoints = 0
        for i in range(0, MAX_LENGTH_SHIP):
            for j in range(i, 4):
                self.maxpoints += i+1

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

    def ustanovka(self, coor_x, coor_y, length, vorh, player):
        if player == 1:
            for i in range(0, length):
                if (vorh == 'h'):
                    self.field[coor_y][coor_x + i][1] = '1'
                else:
                    self.field[coor_y + i][coor_x][1] = '1'
        elif player == 2:
            for i in range(0, length):
                if (vorh == 'h'):
                    self.field[coor_y][coor_x + i][3] = '1'
                else:
                    self.field[coor_y + i][coor_x][3] = '1'

    def user_rasstanovka(self):
        for i in range(1, MAX_LENGTH_SHIP+1):
            for j in range(0, MAX_LENGTH_SHIP+1-i):
                cur_size = i
                coord_x = int(input("Input x: ")) -1
                coord_y = int(input("Input y: ")) -1
                vorh = input("Vertical/horizontal? v/h: ")
                self.ustanovka(coord_x, coord_y, cur_size, vorh, 1)

    def printfield(self):
        for x in range(0, FIELD_SIZE_X):
            for y in range(0, FIELD_SIZE_Y):
                print("".join(self.field[x][y]), end=" ")
            print()

    def fire(self, coor_x, coor_y, player):
        print("Player ", player, " hits in cell (", coor_x+1, ", ", coor_y+1, ")", end="   ")
        if player == 1:
            #проверка кораблей второго игрока
            self.field[coor_y][coor_x][0] = '1'
            if self.field[coor_y][coor_x][3] == '1':
                self.popadeniya1 += 1
                print("HIT")
                return True
            else:
                print("MISS")
                return False
        else:
            self.field[coor_y][coor_x][2] = '1'
            if self.field[coor_y][coor_x][1] == '1':
                self.popadeniya2 += 1
                print("HIT")
                return True
            else:
                print("MISS")
                return False

    def join_user2(self, player2):
        if len(self.players) > 2:
            return False
        self.players.append(Player(player2, 1))


    def computer_initial(self):

        for i in range(1, MAX_LENGTH_SHIP+1):
            print(MAX_LENGTH_SHIP+2-i)
            for j in range(0,MAX_LENGTH_SHIP+1-i):
                cur_size = i
                rand_vorh = random.randint(0, 100) % 2
                if rand_vorh:
                    #horyzontal
                    coord_x = random.randint(1, FIELD_SIZE_X-cur_size) - 1
                    coord_y = random.randint(1, FIELD_SIZE_Y) - 1
                    while self.field[coord_x][coord_y][3] == '1':
                        coord_x = random.randint(1, FIELD_SIZE_X - cur_size) - 1
                        coord_y = random.randint(1, FIELD_SIZE_Y) - 1
                    print("horyz: ", coord_x, coord_y)
                    self.ustanovka(coord_x, coord_y, cur_size, 'h', 2)
                else:
                    coord_x = random.randint(1, FIELD_SIZE_X) - 1
                    coord_y = random.randint(1, FIELD_SIZE_Y - cur_size) - 1
                    while self.field[coord_x][coord_y][3] == '1':
                        coord_x = random.randint(1, FIELD_SIZE_X) - 1
                        coord_y = random.randint(1, FIELD_SIZE_Y - cur_size) - 1
                    print("vert: ", coord_x, coord_y)
                    self.ustanovka(coord_x, coord_y, cur_size, 'v', 2)

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
        
        if 0 <= choosen_y < FIELD_SIZE_Y and FIELD_SIZE_X > choosen_x >= 0:
            self.fire(choosen_x, choosen_y, 1)

    def checker(self):
        if self.maxpoints == self.popadeniya2 or self.maxpoints == self.popadeniya1:
            self.finished = True

    def start_game(self):
        print("The game ", self._id, " has been started with gamers: ", self.players)
        self.running = True
        pointer = 1
        while self.running and not self.finished:
            self.printfield()
            if pointer == 1:
                self.user_gamer()
                pointer = 0
            else:
                self.computer_gamer()
                pointer = 1
        print("STOP GAME")
        print(self.popadeniya1)
        print(self.popadeniya2)

