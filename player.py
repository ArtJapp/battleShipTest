from Ship import Ship
from settings import *


class Player:
    def __init__(self, name, id):
        self._id = id
        self._name = name

        self._hits = 0
        self._fires = 0

        self.ready = False

        self.ships = []

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def __str__(self):
        return self._name

    def set_ships(self, ships):
        for ship in ships:
            print(ship)
            newone = Ship(ship=ship)
            self.ships.append(newone)

    def fire(self, coord_x, coord_y):
        ans = False
        killed = False
        for ship in self.ships:
            answer = ship.fire_ship(coord_x, coord_y)
            if answer:
                if not ship.is_alive():
                    killed = True
                ans = answer
        return (ans, killed)

    def fired(self, hit):
        self._fires += 1
        if hit:
            self._hits += 1

    def still_alive(self):
        ans = False
        for x in self.ships:
            if x.is_alive():
                ans = True
        return ans

    def get_hits(self):
        return self._hits

    def get_fires(self):
        return self._fires

    def get_ships(self):
        answer = []
        for x in self.ships:
            some_dict = x.__str__()
            answer.append(some_dict)
        return answer


# pl = Player(0, "Pushik")
# pl.set_ships([{'size': 2, 'coordinates': [{'x': 3, 'y': 4}, {'x': 3, 'y': 5}]},
#               {'size': 3, 'coordinates': [{'x': 5, 'y': 6}, {'x': 6, 'y': 6}, {'x': 7, 'y': 6}]}])
# pl.get_ships()
# print(pl.ships)
# print(pl.fire(3, 3))
# print(pl.fire(3, 4))
# print(pl.fire(3, 4))
# print(pl.fire(5, 6))
# print(pl.fire(5, 6))
# print(pl.fire(6, 6))
# print(pl.fire(7, 6))
# print(pl.fire(7, 6))
