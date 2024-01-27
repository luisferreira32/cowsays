import pygame as pg
import json

pg.init()

import consts
from animal import Animal
from recorder import Recorder
from gamestate import GameState, handle_event
from pages import MainMenu, page_map

def clip(surface: pg.Surface, x: int, y: int, x_size: int, y_size: int) -> pg.Surface: #Get a part of the image
    handle_surface = surface.copy() #Sprite that will get process later
    clipRect = pg.Rect(x,y,x_size,y_size) #Part of the image
    handle_surface.set_clip(clipRect) #Clip or you can call cropped
    image = surface.subsurface(handle_surface.get_clip()) #Get subsurface
    return image.copy() #Return

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

    while True:
        # process events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

            if event.type == pg.VIDEORESIZE:
                global_game_state.resize((event.w, event.h))
            global_game_state = page_map[global_game_state.current_page].handle_event(event, global_game_state)

        # draw stuff
        # draw_page_map[global_game_state.current_page](screen, global_game_state)
        main_menu_page.draw_page(screen)
        pg.display.flip()

        # handle real-time calculations
        clock.tick(60)


screen = pg.display.set_mode((consts.SCREEN_WIDTH, consts.SCREEN_HEIGHT), pg.RESIZABLE)
clock = pg.time.Clock()

main_game_loop()
pg.quit()
