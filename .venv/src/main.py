# Test

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

# UI Surfaces & Rectangles
play_button_surface = pg.image.load('../graphics/play-button.png').convert()
play_button_rect = play_button_surface.get_rect(center=(SCREEN_WIDTH // 2, 300))
level_select_placeholder_text = ui_font.render('Placeholder - Go to GAMEPLAY GameState', True, 'White')
level_select_placeholder_rect = level_select_placeholder_text.get_rect(center=(SCREEN_WIDTH // 2, 50))

# Visual Defaults
CELL_SIZE = 80

# Main loop
running = True
while running:

    # Detects all user inputs (aka events)
    for event in pg.event.get():
        if event.type == pg.QUIT: # X Button top right of game window
            pg.quit() # Close the window
            exit() # Stop program entirely
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1: # If user pressed left mouse
            if game_state == GameState.MAIN_MENU:
                if play_button_rect.collidepoint(event.pos): # If the click was inside play button rectangle
                    game_state = GameState.LEVEL_SELECT
            elif game_state == GameState.LEVEL_SELECT:
                if level_select_placeholder_rect.collidepoint(event.pos):
                    game_state = GameState.GAMEPLAY

    # --- MAIN MENU GAME STATE ---
    if game_state == GameState.MAIN_MENU:
        screen.blit(background_surface, (0, 0)) # Draw background image
        screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 30))
        screen.blit(play_button_surface, play_button_rect)

    # --- LEVEL SELECT GAME STATE ---
    elif game_state == GameState.LEVEL_SELECT:
        screen.blit(background_surface, (0, 0)) # Draw background image
        screen.blit(level_select_placeholder_text,
                    (SCREEN_WIDTH // 2 - level_select_placeholder_text.get_width() // 2, 50)
                    )

    # --- GAMEPLAY GAME STATE ---
    elif game_state == GameState.GAMEPLAY:
        screen.blit(background_surface, (0, 0)) # Draw background image

        # Gets grid and block objects from load_level_data()
        level_data = load_level_data()
        block_objects = (level_data[0])
        grid = level_data[1]

        # Gets offsets from get_grid_offset()
        offsets = get_grid_offset(grid.columns, grid.rows, CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
        offset_x = offsets[0]
        offset_y = offsets[1]

        # Draws the grid
        draw_grid(screen, grid, CELL_SIZE, offset_x, offset_y)

    else:
        print("ERROR: Invalid GameState: " + game_state)
        pg.quit()
        exit()

    pg.display.update() # Refresh the screen
    clock.tick(MAX_FRAMERATE) # Controls the framerate to maintain 30 fps max
