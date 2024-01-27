import pygame as pg
import init
import consts
from animal import Animal
from recorder import Recorder
from gamestate import GameState
from pages import handle_event, draw_page_map

def main_game_loop():
    # TODO: load animal list from a json config
    global_game_state = GameState(Recorder(), [Animal("cow", "tmp/cow.webp", consts.BACKGROUND_COLOR, consts.FONT_COLOR)])

    while True:
        # process events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            global_game_state = handle_event(event, global_game_state)

        # draw stuff
        draw_page_map[global_game_state.current_page](screen, global_game_state)
        pg.display.flip()

        # handle real-time calculations
        clock.tick(60)

screen = pg.display.set_mode((consts.SCREEN_WIDTH, consts.SCREEN_HEIGHT))
clock = pg.time.Clock()

main_game_loop()
pg.quit()
