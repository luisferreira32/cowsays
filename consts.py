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

FONT = pg.font.SysFont("Mono", 50)



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
    "cow": "assets/animals_wav/cow.wav",
    "dog": "TODO.wav",
    "cat": "TODO.wav",
    "elephant": "TODO.wav",
    "seal": "TODO.wav",
    "giraffe": "TODO.wav",
    "orca": "TODO.wav",
    "human": "TODO.wav",
    "seagull": "TODO.wav",
}