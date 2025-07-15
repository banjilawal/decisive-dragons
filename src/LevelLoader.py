import json
from .Block import *
from .Grid import *
import pygame as pg


# Reads a JSON file and creates grid and block objects
def load_level_data(level_id=1):

    # Builds the correct level file name according to given level_id
    # All level files must be formatted as 'level-#.json'
    level_file_name = 'level-' + str(level_id) + '.json'

    # Saves json file to dict called level_data
    with open('../levels/' + level_file_name, 'r') as file:
        level_data = json.load(file)

    # Creates grid
    grid_data = level_data["grid"] # dict with rows, column, escape_cell as keys
    columns = grid_data["columns"]
    rows = grid_data["rows"]
    escape_cell = grid_data["escape_cell"] # tuple of integers (row, column)
    grid = Grid(columns, rows, escape_cell) # Grid object using values from grid_data dict

    # Create blocks
    blocks_data = level_data["blocks"] # blocks_data is now a list of dicts. each dict represents 1 block
    block_objects = [] # empty list to hold block objects

    # Iterates through blocks_data and adds a block object to block_objects
    for block_info in blocks_data:

        # Saving data from JSON
        block_type = block_info["type"]
        top_left_row, top_left_col = block_info["top_left"]
        btm_right_row, btm_right_col = block_info["btm_right"]

        # Calculates width and height based on position of corners
        # For example: If top left is on row 1 and bottom right is on row 2...
        # ... then 2 - 1 + 1 = 2
        width = btm_right_row - top_left_row + 1
        height = btm_right_col - top_left_col + 1

        # Instantiate new block object based on type
        if block_type == "PrizeBox":
            block = PrizeBox()
        elif block_type == "Box":
            block = Box(top_left_row, top_left_col, width, height)
        elif block_type == "Immovable":
            block = Immovable(top_left_row, top_left_col, width, height)
        elif block_type == "Shelf":
            block = Shelf(top_left_row, top_left_col, width, height)
        else:
            raise ValueError(f"Unknown Block Type: {block_type}")

        # Adds block object to list of block objects
        block_objects.append(block)

    # Returns the list of block objects and the grid object as a tuple
    return block_objects, grid


# Calculates the offsets, which is the space between edge of screen and edge of grid
# This is so the grid can always be centered on the screen
def get_grid_offset(columns, rows, cell_size, screen_width, screen_height):

    # Gets the actual width and height of the grid in pixels
    board_width_px = columns * cell_size
    board_height_px = rows * cell_size

    # Calculates offset based on screen size and grid size
    offset_x = (screen_width - board_width_px) // 2
    offset_y = (screen_height - board_height_px) // 2

    # Returns the two offsets as a tuple
    return offset_x, offset_y


# Draws the grid
def draw_grid(surface, grid, cell_size, offset_x, offset_y):
    for row in range(grid.rows):
        for col in range(grid.columns):
            rect_x = offset_x + row * cell_size
            rect_y = offset_y + col * cell_size
            rect = pg.Rect(rect_x, rect_y, cell_size, cell_size)
            pg.draw.rect(surface, (200, 200, 200), rect, width=1) # Grey lines (temporary)
