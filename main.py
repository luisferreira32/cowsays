import pygame as pg
import json

from typing import Mapping

pg.init()

from cowsays import consts  # noqa: E402
from cowsays.animal import Animal  # noqa: E402
from cowsays.gamestate import GlobalGameState  # noqa: E402
from cowsays.pages import GamePage, MainMenu, ScorePage, RecordingAnimalPage, GameOver  # noqa: E402


def main_game_loop():
    animals = []
    with open("assets/animals.json") as f:
        animals_dict = json.load(f)
        for animal_dict in animals_dict["animals"]:
            animals.append(
                Animal(
                    animal_dict["name"],
                    animal_dict["pixel_art_src"],
                    animal_dict["sound_ref_src"],
                )
            )

    game_state = GlobalGameState(consts.SCREEN_SIZE, animals)

    page_map: Mapping[int, GamePage] = {
        consts.PAGE_SHOW_THE_ANIMAL_RECORDING: RecordingAnimalPage(
            consts.SCREEN_SIZE,
            pg.image.load("assets/sprites/button_rec.png"),
        ),
        consts.PAGE_SHOW_THE_ANIMAL_SCORE: ScorePage(
            consts.SCREEN_SIZE,
            pg.image.load("assets/sprites/button_quit.png"),
            pg.image.load("assets/sprites/button_next.png"),
            pg.image.load("assets/sprites/score_sprite.png"),
        ),
        consts.PAGE_MAIN_MENU: MainMenu(
            consts.SCREEN_SIZE,
            pg.image.load("assets/sprites/cows-say-moo.png"),
            pg.image.load("assets/sprites/button_start.png"),
        ),
        consts.PAGE_GAME_OVER: GameOver(
            consts.SCREEN_SIZE,
            pg.image.load("assets/sprites/button_gameover.png"),
        ),
    }

    while True:
        # process events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

            if event.type == pg.VIDEORESIZE:
                game_state.resize((event.w, event.h))
                for p in page_map.values():
                    p.resize((event.w, event.h))

            if not game_state.preparing_to_beam:
                page_map[game_state.current_page].handle_event(event, game_state)

        # draw stuff
        page_map[game_state.current_page].draw_page(screen, game_state)
        pg.display.flip()

        # handle real-time calculations
        delta = clock.tick(60)
        game_state.update_timers(delta)
        for p in page_map.values():
            p.update_timers(game_state, delta)


screen = pg.display.set_mode((consts.SCREEN_WIDTH, consts.SCREEN_HEIGHT), pg.RESIZABLE)
clock = pg.time.Clock()

main_game_loop()
pg.quit()
