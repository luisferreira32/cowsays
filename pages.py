import pygame as pg
import random

import consts

from gamestate import GameState


def draw_page_show_the_animal_says(screen: pg.Surface, global_game_state: GameState):
    animal = global_game_state.current_animal
    screen.fill(animal.background_color)
    screen.blit(animal.surface, (global_game_state.screen_constraints_w * 1 / 4, global_game_state.screen_constraints_h * 1 / 4))

    record_text = consts.FONT.render(f"The {animal.name} says...", True, consts.FONT_COLOR)
    record_rect = record_text.get_rect(center=(global_game_state.screen_constraints_w / 2, global_game_state.screen_constraints_h - 100))
    screen.blit(record_text, record_rect)


def draw_page_show_the_animal_recording(screen: pg.Surface, global_game_state: GameState):
    animal = global_game_state.current_animal
    screen.fill(animal.background_color)
    screen.blit(animal.surface, (global_game_state.screen_constraints_w * 1 / 4, global_game_state.screen_constraints_h * 1 / 4))

    record_text = consts.FONT.render(f"Recording your {animal.name} sound", True, consts.FONT_COLOR)
    record_rect = record_text.get_rect(center=(global_game_state.screen_constraints_w / 2, global_game_state.screen_constraints_h - 100))
    screen.blit(record_text, record_rect)


def draw_page_show_the_animal_score(screen: pg.Surface, global_game_state: GameState):
    animal = global_game_state.current_animal
    screen.fill(animal.background_color)
    screen.blit(animal.surface, (global_game_state.screen_constraints_w * 1 / 4, global_game_state.screen_constraints_h * 1 / 4))

    score_text = consts.FONT.render(f"Your similarity with the {animal.name} is: {global_game_state.current_evaluation}%", True, consts.FONT_COLOR)
    score_rect = score_text.get_rect(center=(global_game_state.screen_constraints_w / 2, global_game_state.screen_constraints_h - 100))
    screen.blit(score_text, score_rect)

    feedback_text = consts.FONT.render(f"You {'rock!' if global_game_state.current_evaluation >= 60 else 'suck...'}", True, consts.FONT_COLOR)
    feedback_rect = feedback_text.get_rect(center=(global_game_state.screen_constraints_w / 2, global_game_state.screen_constraints_h - 50))
    screen.blit(feedback_text, feedback_rect)


def calculate_similarity(ref: pg.mixer.Sound, recorded: pg.mixer.Sound) -> int:
    # TODO: calculate similarity
    return int(100 * random.random())


def handle_event(event: pg.event.Event, global_game_state: GameState) -> GameState:
    if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and global_game_state.current_page == consts.PAGE_SHOW_THE_ANIMAL_SAYS:
        global_game_state.recorder.start_recording()
        global_game_state.current_page = consts.PAGE_SHOW_THE_ANIMAL_RECORDING
    elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE and global_game_state.current_page == consts.PAGE_SHOW_THE_ANIMAL_RECORDING:
        global_game_state.recorder.stop_recording()
        global_game_state.current_evaluation = calculate_similarity(None, global_game_state.recorder.mix_sound())
        global_game_state.current_page = consts.PAGE_SHOW_THE_ANIMAL_SCORE
    elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE and global_game_state.current_page == consts.PAGE_SHOW_THE_ANIMAL_SCORE:
        # TODO: load next animal!
        global_game_state.current_page = consts.PAGE_SHOW_THE_ANIMAL_SAYS
    return global_game_state


draw_page_map = {
    consts.PAGE_SHOW_THE_ANIMAL_SAYS: draw_page_show_the_animal_says,
    consts.PAGE_SHOW_THE_ANIMAL_RECORDING: draw_page_show_the_animal_recording,
    consts.PAGE_SHOW_THE_ANIMAL_SCORE: draw_page_show_the_animal_score,
}
