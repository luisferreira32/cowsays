import pygame as pg
import random

import consts

from gamestate import GameState


def draw_page_show_the_animal_says(screen: pg.Surface, global_game_state: GameState):
    animal = global_game_state.current_animal
    screen.fill(animal.background_color)
    screen.blit(animal.surface, (global_game_state.screen_constraints_w * 1 / 4, global_game_state.screen_constraints_h * 1 / 4))

    record_text = consts.FONT.render(f"The {animal.name} says...", True, animal.foreground_color)
    record_rect = record_text.get_rect(center=(global_game_state.screen_constraints_w / 2, global_game_state.screen_constraints_h - 100))
    screen.blit(record_text, record_rect)


def draw_page_show_the_animal_recording(screen: pg.Surface, global_game_state: GameState):
    animal = global_game_state.current_animal
    screen.fill(animal.background_color)
    screen.blit(animal.surface, (global_game_state.screen_constraints_w * 1 / 4, global_game_state.screen_constraints_h * 1 / 4))

    record_text = consts.FONT.render(f"Recording your {animal.name} sound", True, animal.foreground_color)
    record_rect = record_text.get_rect(center=(global_game_state.screen_constraints_w / 2, global_game_state.screen_constraints_h - 100))
    screen.blit(record_text, record_rect)


def draw_page_show_the_animal_score(screen: pg.Surface, global_game_state: GameState):
    animal = global_game_state.current_animal
    screen.fill(animal.background_color)
    screen.blit(animal.surface, (global_game_state.screen_constraints_w * 1 / 4, global_game_state.screen_constraints_h * 1 / 4))

    score_text = consts.FONT.render(f"Your similarity with the {animal.name} is: {global_game_state.current_evaluation}%", True, animal.foreground_color)
    score_rect = score_text.get_rect(center=(global_game_state.screen_constraints_w / 2, global_game_state.screen_constraints_h - 100))
    screen.blit(score_text, score_rect)

    feedback_text = consts.FONT.render(f"You {'rock!' if global_game_state.current_evaluation >= 60 else 'suck...'}", True, animal.foreground_color)
    feedback_rect = feedback_text.get_rect(center=(global_game_state.screen_constraints_w / 2, global_game_state.screen_constraints_h - 50))
    screen.blit(feedback_text, feedback_rect)


draw_page_map = {
    consts.PAGE_SHOW_THE_ANIMAL_SAYS: draw_page_show_the_animal_says,
    consts.PAGE_SHOW_THE_ANIMAL_RECORDING: draw_page_show_the_animal_recording,
    consts.PAGE_SHOW_THE_ANIMAL_SCORE: draw_page_show_the_animal_score,
}
