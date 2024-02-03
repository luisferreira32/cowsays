from random import shuffle
from typing import List, Tuple, Mapping, Callable

from cowsays import consts
from cowsays.animal import Animal
from cowsays.super_duper_sound_comparison_ai_algorithm import analyze_sound


class GlobalGameState:
    def __init__(self, screen_constraints: Tuple[int, int], animals: List[Animal]):
        self.screen_constraints = screen_constraints
        self.screen_constraints_w, self.screen_constraints_h = screen_constraints

        self.animals = animals
        shuffle(self.animals)

        self.current_page = consts.PAGE_MAIN_MENU
        self.next_page = 0
        self.time_until_beam = 0
        self.preparing_to_beam = False

        self.score = 0
        self.current_evaluation = 0
        self.is_filling_score_bar = False
        self.current_score_bar_index = 0
        self.timer_score_bar_update = consts.TIMER_SCORE_BAR_STEPS

        self.next_animal()

    def next_animal(self) -> None:
        self.current_animal = self.animals.pop()
        self.current_animal.load_surface(self.screen_constraints)
        self.animals.insert(0, self.current_animal)  # Keep cycling the list
        shuffle(self.animals)

    def resize(self, screen_constraints: Tuple[int, int]):
        self.screen_constraints = screen_constraints
        self.screen_constraints_w, self.screen_constraints_h = screen_constraints
        self.current_animal.resize(screen_constraints)

    def beam_to(self, page: int):
        self.preparing_to_beam = True
        self.next_page = page
        self.time_until_beam = consts.BEAM_TIME

    def update_timers(self, delta: int):
        self.current_animal.update_timers(delta)
        self.time_until_beam = self.time_until_beam - delta

        if self.preparing_to_beam and self.time_until_beam <= 0:
            self.preparing_to_beam = False
            page_state_reset[self.next_page](self)
            self.current_page = self.next_page

        if self.is_filling_score_bar:
            self.timer_score_bar_update = self.timer_score_bar_update - delta
            if self.timer_score_bar_update <= 0:
                self.current_score_bar_index += 1
                self.timer_score_bar_update = consts.TIMER_SCORE_BAR_STEPS
            if self.current_score_bar_index >= int(self.current_evaluation) / 5 - 1:
                self.is_filling_score_bar = False


def _state_reset_page_show_the_animal_recording(game_state: GlobalGameState) -> None:
    game_state.next_animal()


def _state_reset_page_show_the_animal_score(game_state: GlobalGameState) -> None:
    game_state.current_evaluation = analyze_sound(game_state.current_animal.sound_ref_src, "output.wav")
    game_state.is_filling_score_bar = True
    game_state.current_score_bar_index = 0
    if game_state.current_evaluation >= consts.SIMILARITY_THRESHOLD:
        game_state.score += 1


def _state_reset_page_main_menu(game_state: GlobalGameState) -> None:
    game_state.score = 0


def _state_reset_page_game_over(game_state: GlobalGameState) -> None:
    game_state.score = 0
    game_state.next_animal()


page_state_reset: Mapping[int, Callable[[GlobalGameState], None]] = {
    consts.PAGE_SHOW_THE_ANIMAL_RECORDING: _state_reset_page_show_the_animal_recording,
    consts.PAGE_SHOW_THE_ANIMAL_SCORE: _state_reset_page_show_the_animal_score,
    consts.PAGE_MAIN_MENU: _state_reset_page_main_menu,
    consts.PAGE_GAME_OVER: _state_reset_page_game_over,
}
