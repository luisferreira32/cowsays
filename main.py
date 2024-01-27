import pygame as pg
import json

pg.init()

import consts
from animal import Animal
from recorder import Recorder
from gamestate import GameState
from pages import page_map


def main_game_loop():
    animals = []
    with open("animals.json") as f:
        animals_dict = json.load(f)
        for animal_dict in animals_dict["animals"]:
            animals.append(
                Animal(
                    animal_dict["name"],
                    animal_dict["asset_src"],
                    animal_dict["sound_ref_src"],
                    pg.Color(animal_dict["background_color"]),
                    pg.Color(animal_dict["foreground_color"]),
                )
            )

    global_game_state = GameState(Recorder(), animals)

    while True:
        # process events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            global_game_state = page_map[global_game_state.current_page].handle_event(event, global_game_state)

        # draw stuff
        page_map[global_game_state.current_page].draw_page(screen, global_game_state)
        pg.display.flip()

        # handle real-time calculations
        clock.tick(60)


screen = pg.display.set_mode((consts.SCREEN_WIDTH, consts.SCREEN_HEIGHT))
clock = pg.time.Clock()

main_game_loop()
pg.quit()
