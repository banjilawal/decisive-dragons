# Parent class of everything that occupies space on the grid
class Block:
    def __init__(self, row=0, column=0, width=1, height=1):
        self.row = row
        self.column = column
        self.width = width
        self.height = height


# Child of Block, parent of Box and Shelf
# Adds movement variables
class Movable(Block):
    def __init__(self, row=0, column=0, width=1, height=1, horiz_mov=True, verti_mov=True):
        super().__init__(row, column, width, height)
        self.horiz_mov = horiz_mov
        self.verti_mov = verti_mov


# Child of Block but essentially the same as Block
class Immovable(Block):
    def __init__(self, row=0, column=0, width=1, height=1):
        super().__init__(row, column, width, height)


# Child of Movable, parent of PrizeBox
# Forced to always be movable in both directions
class Box(Movable):
    def __init__(self, row=0, column=0, width=1, height=1):
        super().__init__(row, column, width, height, horiz_mov=True, verti_mov=True)


# Child of Movable
# Shelves must be either 1 unit tall or 1 unit wide
# Constructor enforces movement based on dimensions
class Shelf(Movable):
    def __init__(self, row=0, column=0, width=2, height=1):  # defaults to horizontal
        if width != 1 and height != 1:
            raise ValueError("Shelf must be either 1 unit tall or 1 unit wide")

        horiz_mov = width > height
        verti_mov = height > width
        super().__init__(row, column, width, height, horiz_mov, verti_mov)


# Child of Box
# Always 1x1 and movable in both directions
class PrizeBox(Box):
    def __init__(self, row=0, column=0):
        super().__init__(row, column, width=1, height=1)
