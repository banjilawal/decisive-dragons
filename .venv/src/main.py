import pygame as pg
from sys import exit

from GameState import *
from LevelLoader import *
from GridEntity import *


# Initialize pygame
pg.init()

# Framerate Setup
clock = pg.time.Clock()
MAX_FRAMERATE = 30

# Set GameState to Main Menu on startup
game_state = GameState.MAIN_MENU

# Game Window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('UNIT')
icon_surface = pg.image.load('../graphics/icon.png').convert_alpha()
pg.display.set_icon(icon_surface)

# Background surface
background_surface = pg.image.load('../graphics/background.png').convert()

# Fonts
ui_font = pg.font.Font('../font/GrapeSoda.ttf', 30)
title_font = pg.font.Font('../font/HEXAGON_.ttf', 200)

# Title surface
title_surface = title_font.render('UNIT', True, (142, 107, 107))

# Play button
play_button_surface = pg.image.load('../graphics/play-button.png').convert()
play_button_rect = play_button_surface.get_rect(center=(SCREEN_WIDTH // 2, 300))

# Back button
back_button_text = ui_font.render('BACK', True, (142, 107, 107))
back_button_rect = back_button_text.get_rect(topleft=(7, 10))

# Initialize selected_level
selected_level = None

# Initializing empty list for level buttons
level_buttons = []

# Select level list here with the json file
level_select_data = [
    {'id': 1, 'name': 'Level 1'},
    {'id': 2, 'name': 'Level 2'},
    {'id': 3, 'name': 'Level 3'},
    {'id': 4, 'name': 'Level 4'},
    {'id': 5, 'name': 'Level 5'},
    {'id': 6, 'name': 'Level 6'}
]

# Iterates through each level to create list of level buttons to display
for i, level in enumerate(level_select_data):
    level_text = ui_font.render(level['name'], True, 'White')
    level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, 200 + i * 70))
    level_buttons.append({'text_surface': level_text, 'rect': level_rect, 'id': level['id']})

# Visual Defaults
CELL_SIZE = 80
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Block and grid and movement variables initialize
grid = None
block_objects = []
offset_x = 0
offset_y = 0
selected_block = None
drag_offset_x = 0
drag_offset_y = 0

# Main loop
running = True
while running:

    # --- EVENT HANDLERS ---
    for event in pg.event.get():

        # Exit game with window x button
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        # Main Menu Event Handler
        if game_state == GameState.MAIN_MENU:

            # On left click
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if play_button_rect.collidepoint(event.pos): # If the click was inside play button rectangle
                    game_state = GameState.LEVEL_SELECT

        # Level Select Event Handler
        elif game_state == GameState.LEVEL_SELECT:

            # On left click
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:

                # Load level if a level button is clicked
                for button in level_buttons:
                    if button['rect'].collidepoint(event.pos):

                        # Set level variables and go to Gameplay State
                        selected_level = button['id']
                        block_objects, grid = load_level_data(selected_level)
                        offset_x, offset_y = get_grid_offset(grid.columns, grid.rows, CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
                        game_state = GameState.GAMEPLAY
                        break

        # Gameplay Event Handler
        elif game_state == GameState.GAMEPLAY:

            # On left click
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                # Back button handler
                if back_button_rect.collidepoint(event.pos):
                    game_state = GameState.LEVEL_SELECT # Go back to level select

                # Detect Left Click on all Blocks (Grid Entities)
                for block in block_objects:
                    rect = get_block_rect(block, CELL_SIZE, offset_x, offset_y)
                    if rect.collidepoint(event.pos):
                        selected_block = block
                        print(selected_block) # DEBUG

                        # These gives us the mouse click's distance from the top left corner of the block
                        drag_offset_x = event.pos[0] - rect.x
                        drag_offset_y = event.pos[1] - rect.y
                        break

            # On move mouse while a block is selected and holding left click
            elif event.type == pg.MOUSEMOTION and selected_block is not None and pg.mouse.get_pressed()[0]:

                # Find current block top left corner
                mouse_x, mouse_y = event.pos
                block_px_x = mouse_x - drag_offset_x
                block_px_y = mouse_y - drag_offset_y

                # Set new col and row
                new_col = (((block_px_x - offset_x) // CELL_SIZE) + 1)
                new_row = (((block_px_y - offset_y) // CELL_SIZE) + 1)

                # Keeps in bounds
                max_col = grid.columns - selected_block.width + 1
                max_row = grid.rows - selected_block.height + 1
                new_col = max(1, min(new_col, max_col))
                new_row = max(1, min(new_row, max_row))

                # Restricts movements based on booleans
                if isinstance(selected_block, Mover):
                    if selected_block.horiz_mov and not selected_block.verti_mov:
                        selected_block.column = new_col
                    elif selected_block.verti_mov and not selected_block.horiz_mov:
                        selected_block.row = new_row
                    elif selected_block.horiz_mov and selected_block.verti_mov:
                        selected_block.column = new_col
                        selected_block.row = new_row



    # --- MAIN MENU GAME STATE DISPLAY ---
    if game_state == GameState.MAIN_MENU:
        screen.blit(background_surface, (0, 0)) # Draw background image
        screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 30))
        screen.blit(play_button_surface, play_button_rect)

    # --- LEVEL SELECT GAME STATE DISPLAY ---
    elif game_state == GameState.LEVEL_SELECT:
        screen.blit(background_surface, (0, 0)) # Draw background image

        # Displays level buttons
        for button in level_buttons:
            screen.blit(button['text_surface'], button['rect'])

    # --- GAMEPLAY GAME STATE DISPLAY ---
    elif game_state == GameState.GAMEPLAY:
        screen.blit(background_surface, (0, 0)) # Draw background image

        # Draws the back button
        screen.blit(back_button_text, back_button_rect)

        # Draws the grid
        draw_grid(screen, grid, CELL_SIZE, offset_x, offset_y)

        # Draws blocks on grid
        for block in block_objects:
            rect = get_block_rect(block, CELL_SIZE, offset_x, offset_y)
            if isinstance(block, PrizeBox):
                pg.draw.rect(screen, RED, rect)
            elif isinstance(block, Immovable):
                pg.draw.rect(screen, WHITE, rect)
            else:
                pg.draw.rect(screen, BLUE, rect)

    else:
        print("ERROR: Invalid GameState: " + game_state)
        pg.quit()
        exit()

    pg.display.update() # Refresh the screen
    clock.tick(MAX_FRAMERATE) # Controls the framerate to maintain 30 fps max
