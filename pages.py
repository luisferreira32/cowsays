import pygame as pg
from random import random

import consts

from gamestate import GameState

def clip(surface: pg.Surface, x: int, y: int, x_size: int, y_size: int) -> pg.Surface: #Get a part of the image
    handle_surface = surface.copy() #Sprite that will get process later
    clipRect = pg.Rect(x,y,x_size,y_size) #Part of the image
    handle_surface.set_clip(clipRect) #Clip or you can call cropped
    image = surface.subsurface(handle_surface.get_clip()) #Get subsurface
    return image.copy() #Return

def calculate_similarity(ref_path: str | None, recorded_path: str | None) -> int:
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

class MainMenu:
    def __init__(self, global_game_state: GameState, start_button_sprite: pg.Surface):
        self.isStartButtonPressed = False
        self.game_state = global_game_state
        self.sprite_start_button_unpressed = clip(start_button_sprite, 5, 19, 53, 31)

    def draw_page(self, screen: pg.Surface):
        screen.fill(consts.BACKGROUND_COLOR)
        screen.blit(pg.transform.scale_by(self.sprite_start_button_unpressed,5), (self.game_state.screen_constraints_w / 2 , self.game_state.screen_constraints_h / 2))

        
