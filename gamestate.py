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

        self.current_page = consts.PAGE_SHOW_THE_ANIMAL_RECORDING

        self.score = 0
        self.current_evaluation = 0
        self.next_animal()

    def next_animal(self) -> None:
        self.current_animal = self.animals.pop()
        self.current_animal.load_surface(consts.SCREEN_SIZE)
        self.animals.insert(0, self.current_animal)  # Keep cycling the list
        shuffle(self.animals)
