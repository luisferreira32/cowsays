import pygame as pg
from typing import Tuple

from cowsays import consts
from cowsays.recorder import Recorder
from cowsays.gamestate import GlobalGameState


def clip(surface: pg.Surface, x: int, y: int, x_size: int, y_size: int) -> pg.Surface:
    handle_surface = surface.copy()
    clipRect = pg.Rect(x, y, x_size, y_size)
    handle_surface.set_clip(clipRect)
    image = surface.subsurface(handle_surface.get_clip())
    return image.copy()


class GamePage:
    def draw_page(self, _1: pg.Surface, _2: GlobalGameState):
        pass

    def handle_event(self, _: pg.event.Event, game_state: GlobalGameState) -> GlobalGameState:
        return game_state

    def resize(self, _: Tuple[int, int]):
        pass

    def update_timers(self, _1: GlobalGameState, _2: int):
        pass


class RecordingAnimalPage(GamePage):
    def __init__(self, screen_constraints: Tuple[int, int], record_button_sprite: pg.Surface) -> None:
        self.recorder = Recorder()

        screen_constraints_w, screen_constraints_h = screen_constraints
        self.record_button_sprite_unpressed = pg.transform.scale_by(clip(record_button_sprite, 20, 9, 24, 35), 4)
        self.record_button_sprite_pressed = pg.transform.scale_by(clip(record_button_sprite, 84, 9, 24, 35), 4)
        self.record_button_rect = self.record_button_sprite_unpressed.get_rect(center=(screen_constraints_w / 2, screen_constraints_h * 5 / 6))
        self.record_button_pressed = False

    def draw_page(self, screen: pg.Surface, global_game_state: GlobalGameState):
        animal = global_game_state.current_animal
        screen.fill(consts.BACKGROUND_COLOR)
        screen.blit(animal.surface, animal.rect)

        score_text = consts.FONT.render(f"{global_game_state.score}", True, consts.FONT_COLOR)
        score_rect = score_text.get_rect(center=(global_game_state.screen_constraints_w - 50, 50))
        screen.blit(score_text, score_rect)

        screen.blit(self.record_button_sprite_pressed if self.record_button_pressed else self.record_button_sprite_unpressed, self.record_button_rect)

    def handle_event(self, event: pg.event.Event, game_state: GlobalGameState) -> GlobalGameState:
        if (event.type == pg.MOUSEBUTTONDOWN and self.record_button_rect.collidepoint(event.pos)) or (event.type == pg.KEYDOWN and event.key == pg.K_SPACE):
            self.recorder.start_recording()
            self.record_button_pressed = True
        elif (event.type == pg.MOUSEBUTTONUP and self.record_button_pressed is True) or (event.type == pg.KEYUP and event.key == pg.K_SPACE):
            self.recorder.stop_recording()
            self.record_button_pressed = False
            game_state.beam_to(consts.PAGE_SHOW_THE_ANIMAL_SCORE)
        return game_state

    def resize(self, screen_constraints: Tuple[int, int]):
        screen_constraints_w, screen_constraints_h = screen_constraints
        self.record_button_rect = self.record_button_sprite_unpressed.get_rect(center=(screen_constraints_w / 2, screen_constraints_h * 5 / 6))


class ScorePage(GamePage):
    def __init__(self, screen_constraints: Tuple[int, int], quit_button_sprite: pg.Surface, next_button_sprite: pg.Surface, sprite_score: pg.Surface) -> None:
        screen_constraints_w, screen_constraints_h = screen_constraints

        self.sprites_score_bar = [pg.transform.scale_by(clip(sprite_score, 4 + i * 32, 13, 25, 6), 16) for i in range(20)]
        self.rects_score_bar = [sprite.get_rect(center=(screen_constraints_w / 2, screen_constraints_h * 9 / 12)) for sprite in self.sprites_score_bar]

        self.quit_button_sprite_unpressed = pg.transform.scale_by(clip(quit_button_sprite, 5, 19, 53, 31), 4)
        self.quit_button_sprite_pressed = pg.transform.scale_by(clip(quit_button_sprite, 69, 19, 53, 31), 4)
        self.quit_button_rect = self.quit_button_sprite_unpressed.get_rect(center=(screen_constraints_w / 2 - 120, screen_constraints_h * 21 / 24))
        self.quit_button_pressed = False

        self.next_button_sprite_unpressed = pg.transform.scale_by(clip(next_button_sprite, 5, 19, 53, 31), 4)
        self.next_button_sprite_pressed = pg.transform.scale_by(clip(next_button_sprite, 69, 19, 53, 31), 4)
        self.next_button_rect = self.quit_button_sprite_unpressed.get_rect(center=(screen_constraints_w / 2 + 120, screen_constraints_h * 21 / 24))
        self.next_button_pressed = False

    def draw_page(self, screen: pg.Surface, game_state: GlobalGameState):
        animal = game_state.current_animal
        screen.fill(consts.BACKGROUND_COLOR)
        screen.blit(animal.surface, animal.rect)

        score_text = consts.FONT.render(f"{game_state.score}", True, consts.FONT_COLOR)
        score_rect = score_text.get_rect(center=(game_state.screen_constraints_w - 50, 50))
        screen.blit(score_text, score_rect)

        screen.blit(
            self.sprites_score_bar[game_state.current_score_bar_index],
            self.rects_score_bar[game_state.current_score_bar_index],
        )

        if not game_state.is_filling_score_bar:
            screen.blit(self.quit_button_sprite_pressed if self.quit_button_pressed else self.quit_button_sprite_unpressed, self.quit_button_rect)
            screen.blit(self.next_button_sprite_pressed if self.next_button_pressed else self.next_button_sprite_unpressed, self.next_button_rect)

    def handle_event(self, event: pg.event.Event, game_state: GlobalGameState) -> GlobalGameState:
        if (event.type == pg.MOUSEBUTTONDOWN and self.quit_button_rect.collidepoint(event.pos)) or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            self.quit_button_pressed = True
        elif (event.type == pg.MOUSEBUTTONDOWN and self.next_button_rect.collidepoint(event.pos)) or (event.type == pg.KEYDOWN and event.key == pg.K_SPACE):
            self.next_button_pressed = True
        elif (event.type == pg.MOUSEBUTTONUP and self.quit_button_pressed is True) or (event.type == pg.KEYUP and event.key == pg.K_ESCAPE):
            self.quit_button_pressed = False
            game_state.beam_to(consts.PAGE_MAIN_MENU)
        elif (event.type == pg.MOUSEBUTTONUP and self.next_button_pressed is True) or (event.type == pg.KEYUP and event.key == pg.K_SPACE):
            self.next_button_pressed = False
            if game_state.current_evaluation >= consts.SIMILARITY_THRESHOLD:
                game_state.beam_to(consts.PAGE_SHOW_THE_ANIMAL_RECORDING)
            else:
                game_state.beam_to(consts.PAGE_GAME_OVER)
        return game_state

    def resize(self, screen_constraints: Tuple[int, int]):
        screen_constraints_w, screen_constraints_h = screen_constraints
        self.quit_button_rect = self.quit_button_sprite_unpressed.get_rect(center=(screen_constraints_w / 2 - 120, screen_constraints_h * 21 / 24))
        self.next_button_rect = self.quit_button_sprite_unpressed.get_rect(center=(screen_constraints_w / 2 + 120, screen_constraints_h * 21 / 24))
        self.rects_score_bar = [sprite.get_rect(center=(screen_constraints_w / 2, screen_constraints_h * 9 / 12)) for sprite in self.sprites_score_bar]


class MainMenu(GamePage):
    def __init__(self, screen_constraints: Tuple[int, int], main_title_sprite: pg.Surface, start_button_sprite: pg.Surface):
        screen_constraints_w, screen_constraints_h = screen_constraints
        self.main_title_sprite = pg.transform.scale_by(main_title_sprite, 2)
        self.main_title_rect = self.main_title_sprite.get_rect(center=(screen_constraints_w / 2, screen_constraints_h / 4))

        self.sprite_start_button_unpressed = pg.transform.scale_by(clip(start_button_sprite, 5, 19, 53, 31), 5)
        self.sprite_start_button_pressed = pg.transform.scale_by(clip(start_button_sprite, 69, 19, 53, 31), 5)
        self.start_button_rect = self.sprite_start_button_unpressed.get_rect(center=(screen_constraints_w / 2, 3 * screen_constraints_h / 5))

        self.is_start_button_pressed = False

    def draw_page(self, screen: pg.Surface, _: GlobalGameState):
        screen.fill(consts.BACKGROUND_COLOR)
        screen.blit(self.main_title_sprite, self.main_title_rect)
        screen.blit(self.sprite_start_button_pressed if self.is_start_button_pressed else self.sprite_start_button_unpressed, self.start_button_rect)

    def handle_event(self, event: pg.event.Event, game_state: GlobalGameState):
        if (event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.start_button_rect.collidepoint(event.pos)) or (
            event.type == pg.KEYDOWN and event.key == pg.K_SPACE
        ):
            self.is_start_button_pressed = True
        if (event.type == pg.MOUSEBUTTONUP and event.button == 1 and self.is_start_button_pressed) or (event.type == pg.KEYUP and event.key == pg.K_SPACE):
            self.is_start_button_pressed = False
            game_state.beam_to(consts.PAGE_SHOW_THE_ANIMAL_RECORDING)

    def resize(self, screen_constraints: Tuple[int, int]):
        screen_constraints_w, screen_constraints_h = screen_constraints
        self.main_title_rect = self.main_title_sprite.get_rect(center=(screen_constraints_w / 2, screen_constraints_h / 4))
        self.start_button_rect = self.sprite_start_button_unpressed.get_rect(center=(screen_constraints_w / 2, 3 * screen_constraints_h / 5))
        self.start_button_pressed_rect = self.sprite_start_button_pressed.get_rect(center=(screen_constraints_w / 2, 3 * screen_constraints_h / 5))


class GameOver(GamePage):
    def __init__(self, screen_constraints: Tuple[int, int], game_over: pg.Surface):
        screen_constraints_w, screen_constraints_h = screen_constraints
        self.sprite_game_over_off = pg.transform.scale_by(clip(game_over, 14, 50, 99, 21), 7)
        self.sprite_game_over_on = pg.transform.scale_by(clip(game_over, 142, 50, 99, 21), 7)
        self.game_over_rect = self.sprite_game_over_off.get_rect(center=(screen_constraints_w / 2, screen_constraints_h / 2))

        self.timer_game_over_light = consts.GAME_OVER_BLINK_TIME
        self.is_light_on = False

    def update_timers(self, _: GlobalGameState, delta: int):
        self.timer_game_over_light = self.timer_game_over_light - delta
        if self.timer_game_over_light <= 0:
            self.timer_game_over_light = consts.GAME_OVER_BLINK_TIME
            self.is_light_on = not self.is_light_on

    def draw_page(self, screen: pg.Surface, _: GlobalGameState):
        screen.fill(consts.BACKGROUND_COLOR)
        screen.blit(self.sprite_game_over_on if self.is_light_on else self.sprite_game_over_off, self.game_over_rect)

    def handle_event(self, event: pg.event.Event, game_state: GlobalGameState):
        if (event.type == pg.MOUSEBUTTONDOWN and event.button == 1) or (event.type == pg.KEYDOWN and event.key == pg.K_SPACE):
            game_state.beam_to(consts.PAGE_MAIN_MENU)

    def resize(self, screen_constraints: Tuple[int, int]):
        screen_constraints_w, screen_constraints_h = screen_constraints
        self.game_over_rect = self.sprite_game_over_off.get_rect(center=(screen_constraints_w / 2, screen_constraints_h / 2))
