import consts

from animal import Animal
from recorder import Recorder

from typing import List

class GameState:
    def __init__(self, recorder: Recorder, animals: List[Animal]):
        self.screen_constraints = consts.SCREEN_SIZE
        self.screen_constraints_w, self.screen_constraints_h = consts.SCREEN_SIZE

        self.recorder = recorder
        self.animals = animals

        self.current_page = consts.PAGE_SHOW_THE_ANIMAL_SAYS
        self.current_animal = self.next_animal()

        # TODO: keep track of similarities > 60%
        self.score = 0
        # TODO: calculate this when you stop recording
        self.current_evaluation = 0

    def next_animal(self) -> Animal:
        # TODO: we probably want some sort of randomness here
        self.current_animal = self.animals.pop()
        self.current_animal.load_surface(consts.SCREEN_SIZE)
        return self.current_animal
