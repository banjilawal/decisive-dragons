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
#variable that stores the selected level
selected_level = None

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
#level_select_placeholder_text = ui_font.render('Placeholder - Go to GAMEPLAY GameState', True, 'White')
#level_select_placeholder_rect = level_select_placeholder_text.get_rect(center=(SCREEN_WIDTH // 2, 50))

#initializing empty list
level_buttons = []

#select level list here with the json file
level_select_data = [
    {'id': 1, 'name': 'Level 1'},
    {'id': 2, 'name': 'Level 2'},
]

for i, level in enumerate(level_select_data):
    level_text = ui_font.render(level['name'], True, 'White')
    level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, 200 + i * 70))
    level_buttons.append({'text_surface': level_text, 'rect': level_rect, 'id': level['id']})

#Back button for gameplay screen
back_button_text = ui_font.render('BACK', True, (142, 107, 107))
#back button position
back_button_rect = back_button_text.get_rect(topleft=(7,10))

# Visual Defaults
CELL_SIZE = 80
WHITE = [255, 255, 255]

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
                # Check if any level button was clicked
                for button in level_buttons:
                    if button['rect'].collidepoint(event.pos):
                        selected_level = button['id']
                        game_state = GameState.GAMEPLAY
                        break
            elif game_state == GameState.GAMEPLAY:
                #check if back button was clicked
                if back_button_rect.collidepoint(event.pos):
                    game_state = GameState.LEVEL_SELECT #goes back to select level ui

    # --- MAIN MENU GAME STATE ---
    if game_state == GameState.MAIN_MENU:
        screen.blit(background_surface, (0, 0)) # Draw background image
        screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 30))
        screen.blit(play_button_surface, play_button_rect)

    # --- LEVEL SELECT GAME STATE ---
    elif game_state == GameState.LEVEL_SELECT:
        screen.blit(background_surface, (0, 0)) # Draw background image
        for button in level_buttons:
            screen.blit(button['text_surface'], button['rect'])

    # --- GAMEPLAY GAME STATE ---
    elif game_state == GameState.GAMEPLAY:
        screen.blit(background_surface, (0, 0)) # Draw background image

        #draws the back button
        screen.blit(back_button_text, back_button_rect)

        # Gets grid and block objects from load_level_data()
        level_data = load_level_data(selected_level)
        block_objects = (level_data[0])
        grid = level_data[1]

        # Gets offsets from get_grid_offset()
        offsets = get_grid_offset(grid.columns, grid.rows, CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
        offset_x = offsets[0]
        offset_y = offsets[1]

        # Draws the grid
        draw_grid(screen, grid, CELL_SIZE, offset_x, offset_y)
        for block in block_objects:
            rect = pg.Rect(
               block.column * CELL_SIZE + offset_x,
               block.row * CELL_SIZE + offset_y,
               CELL_SIZE * block.width,
               CELL_SIZE * block.height
            )
            pg.draw.rect(screen, WHITE, rect)
            # pygame.display.flip()
            #
    else:
        print("ERROR: Invalid GameState: " + game_state)
        pg.quit()
        exit()

    pg.display.update() # Refresh the screen
    clock.tick(MAX_FRAMERATE) # Controls the framerate to maintain 30 fps max
