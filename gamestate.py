import pygame as pg
from random import shuffle, random
from typing import List

import consts

from animal import Animal
from recorder import Recorder


class GameState:
    def __init__(self, recorder: Recorder, animals: List[Animal]):
        self.screen_constraints = consts.SCREEN_SIZE
        self.screen_constraints_w, self.screen_constraints_h = consts.SCREEN_SIZE

        self.recorder = recorder
        self.animals = animals
        shuffle(self.animals)

        self.current_page = consts.PAGE_SHOW_THE_ANIMAL_SAYS

        self.score = 0
        self.current_evaluation = 0
        self.next_animal()

    def next_animal(self) -> None:
        self.current_animal = self.animals.pop()
        self.current_animal.load_surface(consts.SCREEN_SIZE)
        self.animals.insert(0, self.current_animal)  # Keep cycling the list
        shuffle(self.animals)


def calculate_similarity(ref_path: str, recorded_path: str) -> int:
    # TODO: calculate similarity
    return int(100 * random())


def handle_event(event: pg.event.Event, global_game_state: GameState) -> GameState:
    if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and global_game_state.current_page == consts.PAGE_SHOW_THE_ANIMAL_SAYS:
        global_game_state.recorder.start_recording()
        global_game_state.current_page = consts.PAGE_SHOW_THE_ANIMAL_RECORDING
    elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE and global_game_state.current_page == consts.PAGE_SHOW_THE_ANIMAL_RECORDING:
        global_game_state.recorder.stop_recording()
        global_game_state.current_evaluation = calculate_similarity(None, None)
        global_game_state.current_page = consts.PAGE_SHOW_THE_ANIMAL_SCORE
    elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE and global_game_state.current_page == consts.PAGE_SHOW_THE_ANIMAL_SCORE:
        if global_game_state.current_evaluation >= 60:
            global_game_state.score += 1
            # TODO: show gameover page and reset score on score < 60
        global_game_state.next_animal()
        global_game_state.current_page = consts.PAGE_SHOW_THE_ANIMAL_SAYS

    return global_game_state
