
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
        coords = someship['coords']
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
        answer = dict()
        answer['alive'] = self.is_alive()
        answer['coords'] = []
        for cell in self._cells:
            temp_dict = dict()
            temp_dict['x'], temp_dict['y'], is_bitten = cell.__str__()
            temp_dict['alive'] = not is_bitten
            answer['coords'].append(temp_dict)
        answer['size'] = len(self._cells)
        return answer

