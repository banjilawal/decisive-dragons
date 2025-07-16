import json
import pygame as pg

from GridEntity import (
    PrizeBox,
    Immovable,
    UniversalMover,
    HorizontalMover,
    VerticalMover
)
from Grid import Grid


# Reads a JSON file and creates grid and block objects
def load_level_data(level_id=1):
    # Build the correct level file name
    level_file_name = f'level-{level_id}.json'

    # Load the JSON level data
    with open('../levels/' + level_file_name, 'r') as file:
        level_data = json.load(file)

    # Extract grid info
    grid_data = level_data["grid"]
    columns = grid_data["columns"]
    rows = grid_data["rows"]
    escape_cell = tuple(grid_data["escape_cell"])
    grid = Grid(columns, rows, escape_cell)

    # Parse block data
    blocks_data = level_data["blocks"]
    block_objects = []

    for block_info in blocks_data:
        block_type = block_info["type"]
        top_left_row, top_left_col = block_info["top_left"]
        btm_right_row, btm_right_col = block_info["btm_right"]

        width = btm_right_col - top_left_col + 1
        height = btm_right_row - top_left_row + 1

        if block_type == "PrizeBox":
            block = PrizeBox(top_left_row, top_left_col)

        elif block_type == "Box":
            block = UniversalMover(top_left_row, top_left_col, width, height)

        elif block_type == "Immovable":
            block = Immovable(top_left_row, top_left_col, width, height)

        elif block_type == "Shelf":
            # Decide direction based on dimensions
            if width > height:
                block = HorizontalMover(top_left_row, top_left_col, width=width)
            elif height > width:
                block = VerticalMover(top_left_row, top_left_col, height=height)
            else:
                raise ValueError("Shelf must be either wider or taller, not square.")

        else:
            raise ValueError(f"Unknown Block Type: {block_type}")

        block_objects.append(block)

    return block_objects, grid


# Calculates the screen offset to center the grid
def get_grid_offset(columns, rows, cell_size, screen_width, screen_height):
    board_width_px = columns * cell_size
    board_height_px = rows * cell_size
    offset_x = (screen_width - board_width_px) // 2
    offset_y = (screen_height - board_height_px) // 2
    return offset_x, offset_y


# Draws the grid lines
def draw_grid(surface, grid, cell_size, offset_x, offset_y):
    for row in range(grid.rows):
        for col in range(grid.columns):
            rect_x = offset_x + col * cell_size  # COLUMN is X
            rect_y = offset_y + row * cell_size  # ROW is Y
            rect = pg.Rect(rect_x, rect_y, cell_size, cell_size)
            pg.draw.rect(surface, (200, 200, 200), rect, width=1)  # Light gray grid lines


def get_block_rect(block, CELL_SIZE, offset_x, offset_y):
    return pg.Rect(
        (CELL_SIZE * (block.column - 1)) + offset_x,
        (CELL_SIZE * (block.row - 1)) + offset_y,
        CELL_SIZE * block.width,
        CELL_SIZE * block.height
    )
