import pygame as pg
from random import random

import consts

from gamestate import GameState


def calculate_similarity(ref_path: str, recorded_path: str) -> int:
    # TODO: calculate similarity - import this
    return int(100 * random())


class RecordingAnimalPage:
    def __init__(self) -> None:
        pass

    def draw_page(self, screen: pg.Surface, global_game_state: GameState):
        animal = global_game_state.current_animal
        screen.fill(animal.background_color)
        screen.blit(animal.surface, (global_game_state.screen_constraints_w * 1 / 4, global_game_state.screen_constraints_h * 1 / 4))

        record_text = consts.FONT.render(f"The {animal.name} says...", True, animal.foreground_color)
        record_rect = record_text.get_rect(center=(global_game_state.screen_constraints_w / 2, global_game_state.screen_constraints_h - 100))
        screen.blit(record_text, record_rect)

    def handle_event(self, event: pg.event.Event, global_game_state: GameState) -> GameState:
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            global_game_state.recorder.start_recording()
        elif event.type == pg.KEYUP and event.key == pg.K_SPACE:
            global_game_state.recorder.stop_recording()
            global_game_state.current_evaluation = calculate_similarity(None, None)
            global_game_state.current_page = consts.PAGE_SHOW_THE_ANIMAL_SCORE
        return global_game_state


class ScorePage:
    def __init__(self) -> None:
        pass

    def draw_page(self, screen: pg.Surface, global_game_state: GameState):
        animal = global_game_state.current_animal
        screen.fill(animal.background_color)
        screen.blit(animal.surface, (global_game_state.screen_constraints_w * 1 / 4, global_game_state.screen_constraints_h * 1 / 4))

        score_text = consts.FONT.render(f"Your similarity with the {animal.name} is: {global_game_state.current_evaluation}%", True, animal.foreground_color)
        score_rect = score_text.get_rect(center=(global_game_state.screen_constraints_w / 2, global_game_state.screen_constraints_h - 100))
        screen.blit(score_text, score_rect)

        feedback_text = consts.FONT.render(f"You {'rock!' if global_game_state.current_evaluation >= 60 else 'suck...'}", True, animal.foreground_color)
        feedback_rect = feedback_text.get_rect(center=(global_game_state.screen_constraints_w / 2, global_game_state.screen_constraints_h - 50))
        screen.blit(feedback_text, feedback_rect)

    def handle_event(self, event: pg.event.Event, global_game_state: GameState) -> GameState:
        if event.type == pg.KEYUP and event.key == pg.K_SPACE:
            if global_game_state.current_evaluation >= 60:
                global_game_state.score += 1
                # TODO: show gameover page and reset score on score < 60
            global_game_state.next_animal()
            global_game_state.current_page = consts.PAGE_SHOW_THE_ANIMAL_RECORDING
        return global_game_state


page_map = {
    consts.PAGE_SHOW_THE_ANIMAL_RECORDING: RecordingAnimalPage(),
    consts.PAGE_SHOW_THE_ANIMAL_SCORE: ScorePage(),
}
