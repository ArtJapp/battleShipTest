
class Cell:
    def __init__(self, coord_x, coord_y):
        self._coord_x = coord_x
        self._coord_y = coord_y

        self._bitten = False

    def is_that_cell(self, coord_x, coord_y):
        if self._coord_x == coord_x and self._coord_y == coord_y:
            return True
        else:
            return False

    def push_cell(self):
        self._bitten = True

    def is_alive(self):
        return not self._bitten

    def __str__(self):
        return (self._coord_x, self._coord_y, self._bitten)


class Ship:
    def __init__(self, **kwargs):
        someship = kwargs['ship']
        self._is_alive = True
        self._length = someship['size']
        coords = someship['coordinates']
        self._cells = []
        for x in coords:
            coord_x = x['x']
            coord_y = x['y']
            self._cells.append(Cell(coord_x=coord_x, coord_y=coord_y))

    def fire_ship(self, coord_x, coord_y):
        answer = False
        alive = False
        for x in self._cells:
            if x.is_that_cell(coord_x=coord_x, coord_y=coord_y) and x.is_alive():
                answer = True
                x.push_cell()
        for x in self._cells:
            alive = alive or x.is_alive()
        if not alive:
            self._is_alive = False
        return answer

    def is_alive(self):
        return self._is_alive

    def __str__(self):
        attres = vars(self)
        return attres


#shipik = Ship(size=2, coordinates=[{'x': 3, 'y': 4}, {'x': 3, 'y': 5}])
#print(shipik.is_alive())
#print(shipik.fire_ship(4, 5))
#print(shipik.fire_ship(3, 4))
#print(shipik.is_alive())
#print(shipik.fire_ship(3, 4))
#print(shipik.is_alive())
#print(shipik.fire_ship(3, 5))
#print(shipik.is_alive())


