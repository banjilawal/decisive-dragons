import pygame as pg
from sys import exit

from GameState import *
from LevelLoader import *


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

    # --- EVENT HANDLER ---
    for event in pg.event.get():

        # Exit game with window x button
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        # Detect Left Mouse Click
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:

            # Main Menu Left Mouse Click Handler
            if game_state == GameState.MAIN_MENU:
                if play_button_rect.collidepoint(event.pos): # If the click was inside play button rectangle
                    game_state = GameState.LEVEL_SELECT

            # Level Select Left Mouse Click Handler
            elif game_state == GameState.LEVEL_SELECT:

                # Load level if a level button is clicked
                for button in level_buttons:
                    if button['rect'].collidepoint(event.pos):

                        # Set level variables and go to Gameplay State
                        selected_level = button['id']
                        block_objects, grid = load_level_data(selected_level)
                        offset_x, offset_y = get_grid_offset(grid.columns, grid.rows, CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
                        game_state = GameState.GAMEPLAY
                        break

            # Gameplay Left Mouse Click Handler
            elif game_state == GameState.GAMEPLAY:

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
            pg.draw.rect(screen, WHITE, rect)

    else:
        print("ERROR: Invalid GameState: " + game_state)
        pg.quit()
        exit()

    pg.display.update() # Refresh the screen
    clock.tick(MAX_FRAMERATE) # Controls the framerate to maintain 30 fps max
