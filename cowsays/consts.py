import pygame as pg

# Game logic consts
SIMILARITY_THRESHOLD = 60


# Screen related sizes
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (1400, 1000)


# Color palet
BACKGROUND_COLOR = pg.Color("palegreen3")
FONT_COLOR = pg.Color("black")


# Game pages
PAGE_MAIN_MENU = 0
PAGE_SHOW_THE_ANIMAL_RECORDING = 1
PAGE_SHOW_THE_ANIMAL_SCORE = 2
PAGE_GAME_OVER = 3


# Font
FONT = pg.font.SysFont("Mono", 40)


# Timers
BEAM_TIME = 300  # Time it takes to transition between pages in miliseconds
GAME_OVER_BLINK_TIME = 500  # Game over screen blinking time
TIMER_SCORE_BAR_STEPS = 100
ANIMAL_JUMP_TIME = 500
