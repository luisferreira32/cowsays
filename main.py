import pygame as pg
import json

pg.init()

import consts
from animal import Animal
from recorder import Recorder
from gamestate import GameState
from pages import MainMenu, ScorePage, RecordingAnimalPage


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

    main_menu_page = MainMenu(global_game_state, pg.image.load("assets/sprites/button_start.png"))

    page_map = {
        consts.PAGE_SHOW_THE_ANIMAL_RECORDING: RecordingAnimalPage(
            global_game_state.screen_constraints,
            pg.image.load("assets/sprites/button_rec.png"),
        ),
        consts.PAGE_SHOW_THE_ANIMAL_SCORE: ScorePage(
            global_game_state.screen_constraints,
            pg.image.load("assets/sprites/button_quit.png"),
            pg.image.load("assets/sprites/button_next.png"),
        ),
        consts.PAGE_MAIN_MENU: MainMenu(global_game_state, pg.image.load("assets/sprites/button_start.png"))
    }

    while True:
        # process events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

            if event.type == pg.VIDEORESIZE:
                global_game_state.resize((event.w, event.h))

            page_map[global_game_state.current_page].handle_event(event, global_game_state)

        # draw stuff
        page_map[global_game_state.current_page].draw_page(screen, global_game_state)
        # main_menu_page.draw_page(screen)
        pg.display.flip()

        # handle real-time calculations
        clock.tick(60)


screen = pg.display.set_mode((consts.SCREEN_WIDTH, consts.SCREEN_HEIGHT), pg.RESIZABLE)
clock = pg.time.Clock()

main_game_loop()
pg.quit()
