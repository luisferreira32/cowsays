import pygame as pg
from random import random
from typing import Tuple
from os import linesep

import consts

from gamestate import GameState
from super_duper_sound_comparison_ai_algorithm import analyze_sound


def clip(surface: pg.Surface, x: int, y: int, x_size: int, y_size: int) -> pg.Surface:
    handle_surface = surface.copy()
    clipRect = pg.Rect(x, y, x_size, y_size)
    handle_surface.set_clip(clipRect)
    image = surface.subsurface(handle_surface.get_clip())
    return image.copy()


class RecordingAnimalPage:
    def __init__(self, screen_constraints: Tuple[int, int], record_button_sprite: pg.Surface) -> None:
        screen_constraints_w, screen_constraints_h = screen_constraints

        self.record_button_sprite_unpressed = pg.transform.scale_by(clip(record_button_sprite, 20, 9, 24, 35), 4)
        self.record_button_sprite_pressed = pg.transform.scale_by(clip(record_button_sprite, 84, 9, 24, 35), 4)
        self.record_button_rect = self.record_button_sprite_unpressed.get_rect(center=(screen_constraints_w / 2, screen_constraints_h * 5 / 6))
        self.record_button_pressed = False

    def draw_page(self, screen: pg.Surface, global_game_state: GameState):
        animal = global_game_state.current_animal
        screen.fill(animal.background_color)
        screen.blit(animal.surface, (global_game_state.screen_constraints_w * 1 / 4, global_game_state.screen_constraints_h * 1 / 4))

        score_text = consts.FONT.render(f"Score: {global_game_state.score}", True, animal.foreground_color)
        score_rect = score_text.get_rect(center=(global_game_state.screen_constraints_w - 300, 50))
        screen.blit(score_text, score_rect)

        record_text = consts.FONT.render(f"The {animal.name} says...", True, animal.foreground_color)
        record_rect = record_text.get_rect(center=(global_game_state.screen_constraints_w / 2, global_game_state.screen_constraints_h * 16 / 17))
        screen.blit(record_text, record_rect)

        screen.blit(
            self.record_button_sprite_pressed,
            self.record_button_rect,
        ) if self.record_button_pressed else screen.blit(
            self.record_button_sprite_unpressed,
            self.record_button_rect,
        )

    def handle_event(self, event: pg.event.Event, global_game_state: GameState) -> GameState:
        if (event.type == pg.MOUSEBUTTONDOWN and self.record_button_rect.collidepoint(event.pos)) or (event.type == pg.KEYDOWN and event.key == pg.K_SPACE):
            global_game_state.recorder.start_recording()
            self.record_button_pressed = True
        elif (event.type == pg.MOUSEBUTTONUP and self.record_button_pressed == True) or (event.type == pg.KEYUP and event.key == pg.K_SPACE):
            global_game_state.recorder.stop_recording()
            self.record_button_pressed = False
            global_game_state.current_evaluation = analyze_sound(global_game_state.current_animal.sound_ref_src, "output.wav")
            global_game_state.beam_to(consts.PAGE_SHOW_THE_ANIMAL_SCORE)
        return global_game_state

    def resize(self, screen_constraints: Tuple[int, int]):
        screen_constraints_w, screen_constraints_h = screen_constraints
        self.record_button_rect = self.record_button_sprite_unpressed.get_rect(center=(screen_constraints_w / 2, screen_constraints_h * 5 / 6))


class ScorePage:
    def __init__(self, screen_constraints: Tuple[int, int], quit_button_sprite: pg.Surface, next_button_sprite: pg.Surface) -> None:
        screen_constraints_w, screen_constraints_h = screen_constraints

        self.quit_button_sprite_unpressed = pg.transform.scale_by(clip(quit_button_sprite, 5, 19, 53, 31), 4)
        self.quit_button_sprite_pressed = pg.transform.scale_by(clip(quit_button_sprite, 69, 19, 53, 31), 4)
        self.quit_button_rect = self.quit_button_sprite_unpressed.get_rect(center=(screen_constraints_w / 2 - 120, screen_constraints_h * 5 / 6))
        self.quit_button_pressed = False

        self.next_button_sprite_unpressed = pg.transform.scale_by(clip(next_button_sprite, 5, 19, 53, 31), 4)
        self.next_button_sprite_pressed = pg.transform.scale_by(clip(next_button_sprite, 69, 19, 53, 31), 4)
        self.next_button_rect = self.quit_button_sprite_unpressed.get_rect(center=(screen_constraints_w / 2 + 120, screen_constraints_h * 5 / 6))
        self.next_button_pressed = False

    def draw_page(self, screen: pg.Surface, global_game_state: GameState):
        animal = global_game_state.current_animal
        screen.fill(animal.background_color)
        screen.blit(animal.surface, (global_game_state.screen_constraints_w * 1 / 4, global_game_state.screen_constraints_h * 1 / 4))

        score_text = consts.FONT.render(f"Score: {global_game_state.score}", True, animal.foreground_color)
        score_rect = score_text.get_rect(center=(global_game_state.screen_constraints_w - 300, 50))
        screen.blit(score_text, score_rect)

        similarity_score_text = consts.FONT.render(
            f"Your similarity with the {animal.name} is: {global_game_state.current_evaluation}%. You {'rock!' if global_game_state.current_evaluation >= 60 else 'suck...'}", True, animal.foreground_color
        )
        similarity_score_rect = similarity_score_text.get_rect(
            center=(global_game_state.screen_constraints_w / 2, global_game_state.screen_constraints_h * 16 / 17)
        )
        screen.blit(similarity_score_text, similarity_score_rect)

        screen.blit(
            self.quit_button_sprite_pressed,
            self.quit_button_rect,
        ) if self.quit_button_pressed else screen.blit(
            self.quit_button_sprite_unpressed,
            self.quit_button_rect,
        )

        screen.blit(
            self.next_button_sprite_pressed,
            self.next_button_rect,
        ) if self.next_button_pressed else screen.blit(
            self.next_button_sprite_unpressed,
            self.next_button_rect,
        )

    def handle_event(self, event: pg.event.Event, global_game_state: GameState) -> GameState:
        if (event.type == pg.MOUSEBUTTONDOWN and self.quit_button_rect.collidepoint(event.pos)) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            self.quit_button_pressed = True
        elif (event.type == pg.MOUSEBUTTONDOWN and self.next_button_rect.collidepoint(event.pos)) or (event.type == pg.KEYDOWN and event.key == pg.K_SPACE):
            self.next_button_pressed = True
        elif (event.type == pg.MOUSEBUTTONUP and self.quit_button_pressed == True) or (event.type == pg.KEYUP and event.key == pg.K_ESCAPE):
            self.quit_button_pressed = False
            global_game_state.score = 0
            global_game_state.beam_to(consts.PAGE_MAIN_MENU)
        elif (event.type == pg.MOUSEBUTTONUP and self.next_button_pressed == True) or (event.type == pg.KEYUP and event.key == pg.K_SPACE):
            self.next_button_pressed = False
            if global_game_state.current_evaluation >= 60:
                global_game_state.score += 1
                global_game_state.next_animal()
                global_game_state.beam_to(consts.PAGE_SHOW_THE_ANIMAL_RECORDING)
            else:
                global_game_state.score = 0
                global_game_state.beam_to(consts.PAGE_GAME_OVER)
                # TODO: show gameover page and reset score on score < 60 and reset there
        return global_game_state

    def resize(self, screen_constraints: Tuple[int, int]):
        screen_constraints_w, screen_constraints_h = screen_constraints
        self.quit_button_rect = self.quit_button_sprite_unpressed.get_rect(center=(screen_constraints_w / 2 - 120, screen_constraints_h * 5 / 6))
        self.next_button_rect = self.next_button_sprite_unpressed.get_rect(center=(screen_constraints_w / 2 + 120, screen_constraints_h * 5 / 6))


class MainMenu:
    def __init__(self, state: GameState, main_title_sprite: pg.Surface, start_button_sprite: pg.Surface):
        self.main_title_sprite = pg.transform.scale_by(main_title_sprite, 2)
        self.main_title_rect = self.main_title_sprite.get_rect(center=(state.screen_constraints_w / 2, state.screen_constraints_h / 4))
        self.is_start_button_pressed = False
        self.sprite_start_button_unpressed = pg.transform.scale_by(clip(start_button_sprite, 5, 19, 53, 31), 5)
        self.sprite_start_button_pressed = pg.transform.scale_by(clip(start_button_sprite, 69, 19, 53, 31), 5)
        self.start_button_unpressed_rect = self.sprite_start_button_unpressed.get_rect(
            center=(state.screen_constraints_w / 2, 3 * state.screen_constraints_h / 5)
        )
        self.start_button_pressed_rect = self.sprite_start_button_pressed.get_rect(center=(state.screen_constraints_w / 2, 3 * state.screen_constraints_h / 5))

    def draw_page(self, screen: pg.Surface, state: GameState):
        screen.fill(consts.BACKGROUND_COLOR)
        screen.blit(self.main_title_sprite, self.main_title_rect)
        if self.is_start_button_pressed:
            screen.blit(self.sprite_start_button_pressed, self.start_button_pressed_rect)
        else:
            screen.blit(self.sprite_start_button_unpressed, self.start_button_unpressed_rect)

    def handle_event(self, event: pg.event.Event, state: GameState):
        if (event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.start_button_unpressed_rect.collidepoint(event.pos)) or (
            event.type == pg.KEYDOWN and event.key == pg.K_SPACE
        ):
            self.is_start_button_pressed = True
        if (event.type == pg.MOUSEBUTTONUP and event.button == 1 and self.is_start_button_pressed) or (event.type == pg.KEYUP and event.key == pg.K_SPACE):
            self.is_start_button_pressed = False
            state.beam_to(consts.PAGE_SHOW_THE_ANIMAL_RECORDING)

    def resize(self, screen_constraints: Tuple[int, int]):
        screen_constraints_w, screen_constraints_h = screen_constraints
        self.main_title_rect = self.main_title_sprite.get_rect(center=(screen_constraints_w / 2, screen_constraints_h / 4))
        self.start_button_unpressed_rect = self.sprite_start_button_unpressed.get_rect(center=(screen_constraints_w / 2, 3 * screen_constraints_h / 5))
        self.start_button_pressed_rect = self.sprite_start_button_pressed.get_rect(center=(screen_constraints_w / 2, 3 * screen_constraints_h / 5))


class GameOver:
    def __init__(self, global_game_state: GameState, game_over: pg.Surface):
        self.game_over = pg.transform.scale_by(game_over, 5)
        self.game_over_rect = self.game_over.get_rect(center=(global_game_state.screen_constraints_w / 2, global_game_state.screen_constraints_h / 2))

        self.sprite_game_over_off = pg.transform.scale_by(clip(game_over, 14, 50, 99, 21), 7)
        self.rect_game_over_off = self.sprite_game_over_off.get_rect(
            center=(global_game_state.screen_constraints_w / 2, global_game_state.screen_constraints_h / 2)
        )
        self.sprite_game_over_on = pg.transform.scale_by(clip(game_over, 142, 50, 99, 21), 7)
        self.rect_game_over_on = self.sprite_game_over_on.get_rect(
            center=(global_game_state.screen_constraints_w / 2, global_game_state.screen_constraints_h / 2)
        )

        self.timer_game_over_light = consts.GAME_OVER_BLINK_TIME
        self.isLightOn = False

    def update_timers(self, delta: int):
        self.timer_game_over_light = self.timer_game_over_light - delta
        if self.timer_game_over_light <= 0:
            self.timer_game_over_light = consts.GAME_OVER_BLINK_TIME
            self.isLightOn = not self.isLightOn

    def draw_page(self, screen: pg.Surface, global_game_state: GameState):
        screen.fill(consts.BACKGROUND_COLOR)
        if self.isLightOn:
            screen.blit(self.sprite_game_over_on, self.rect_game_over_on)
        else:
            screen.blit(self.sprite_game_over_off, self.rect_game_over_off)

    def handle_event(self, event: pg.event.Event, global_game_state: GameState):
        if (event.type == pg.MOUSEBUTTONDOWN and event.button == 1) or (event.type == pg.KEYDOWN and event.key == pg.K_SPACE):
            global_game_state.current_page = consts.PAGE_MAIN_MENU

    def resize(self, screen_constraints: Tuple[int, int]):
        screen_constraints_w, screen_constraints_h = screen_constraints
        self.game_over_rect = self.game_over.get_rect(center=(screen_constraints_w / 2, screen_constraints_h / 2))
