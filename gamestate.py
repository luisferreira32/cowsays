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
        for animal in self.animals:
            animal.resize(screen_constraints)
