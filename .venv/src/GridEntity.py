# Base class for all objects that occupy space on the grid
class GridEntity:
    def __init__(self, row=0, column=0, width=1, height=1):
        self.row = row
        self.column = column
        self.width = width
        self.height = height


# Adds movement capability; base class for all movable entities
class Mover(GridEntity):
    def __init__(self, row=0, column=0, width=1, height=1, horiz_mov=True, verti_mov=True):
        super().__init__(row, column, width, height)
        self.horiz_mov = horiz_mov
        self.verti_mov = verti_mov


# Non-movable block; behaves like a wall or obstacle
class Immovable(GridEntity):
    def __init__(self, row=0, column=0, width=1, height=1):
        super().__init__(row, column, width, height)


# Fully movable block; parent of PrizeBox
class UniversalMover(Mover):
    def __init__(self, row=0, column=0, width=1, height=1):
        super().__init__(row, column, width, height, horiz_mov=True, verti_mov=True)


# Movable only in the horizontal direction; must be wider than it is tall
class HorizontalMover(Mover):
    def __init__(self, row=0, column=0, width=2):
        super().__init__(row, column, width, height=1, horiz_mov=True, verti_mov=False)


# Movable only in the vertical direction; must be taller than it is wide
class VerticalMover(Mover):
    def __init__(self, row=0, column=0, height=2):
        super().__init__(row, column, width=1, height=height, horiz_mov=False, verti_mov=True)


# A special 1x1 fully movable block; used as the win condition
class PrizeBox(UniversalMover):
    def __init__(self, row=0, column=0):
        super().__init__(row, column, width=1, height=1)
