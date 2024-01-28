from random import shuffle
from typing import List, Tuple

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

        self.current_page = consts.PAGE_MAIN_MENU
        self.next_page = 0
        self.time_until_beam = 0
        self.preparing_to_beam = False

        self.score = 0
        self.current_evaluation = 0
        self.next_animal()

    def next_animal(self) -> None:
        self.current_animal = self.animals.pop()
        self.current_animal.load_surface(self.screen_constraints)
        self.animals.insert(0, self.current_animal)  # Keep cycling the list
        shuffle(self.animals)

    def resize(self, screen_constraints: Tuple[int, int]):
        self.screen_constraints = screen_constraints
        self.screen_constraints_w, self.screen_constraints_h = screen_constraints

    def beam_to(self, page: int):
        self.preparing_to_beam = True
        self.next_page = page
        self.time_until_beam = consts.BEAM_TIME

    def update_beam_timer(self, delta: int):
        self.time_until_beam = self.time_until_beam - delta

        if self.preparing_to_beam and self.time_until_beam <= 0:
            self.preparing_to_beam = False
            self.current_page = self.next_page
