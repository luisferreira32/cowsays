import pygame as pg

# Screen related sizes
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (1800, 1200)

# Color palet
BACKGROUND_COLOR = pg.Color("palegreen3")
FONT_COLOR = pg.Color("black")

# Game pages
PAGE_MAIN_MENU = 0
PAGE_SHOW_THE_ANIMAL_RECORDING = 1
PAGE_SHOW_THE_ANIMAL_SCORE = 2
PAGE_GAME_OVER = 3

FONT = pg.font.SysFont("Mono", 50)

# Time it takes to transition between pages in miliseconds
BEAM_TIME = 300

# Game over screen blinking time
GAME_OVER_BLINK_TIME = 500

TIMER_SCORE_BAR_STEPS = 100

ANIMALS = [
    "chicken",
    "cow",
    "dog",
    "cat",
    "elephant",
    "seal",
    "giraffe", 
    "orca",
    "human",
    "seagull",
    ]

ANIMAL_WAVS = {
    "chicken": "TODO.wav",
    "cow": "TODO.wav",
    "dog": "TODO.wav",
    "cat": "TODO.wav",
    "elephant": "TODO.wav",
    "seal": "TODO.wav",
    "giraffe": "TODO.wav",
    "orca": "TODO.wav",
    "human": "TODO.wav",
    "seagull": "TODO.wav",
}
