import pygame as pg
from typing import Tuple

import consts


class Animal:
    def __init__(self, name: str, pixel_art_src: str, sound_ref_src: str, background_color: pg.Color, foreground_color: pg.Color):
        self.name = name
        self.pixel_art_src = pixel_art_src
        self.sound_ref_src = sound_ref_src
        self.surface_w, self.surface_h = 0, 0
        self.background_color = background_color
        self.foreground_color = foreground_color

        self.timer_animal_jump = consts.ANIMAL_JUMP_TIME
        self.is_jumping = False

        self.loaded = False

    def load_surface(self, screen_constraints: Tuple[int, int]):
        self.surface = pg.image.load(self.pixel_art_src)
        self.surface_w, self.surface_h = self.surface.get_size()
        self.loaded = True
        self.resize(screen_constraints)
        self.rect = self.surface.get_rect(center=(screen_constraints[0] / 2, screen_constraints[1] / 2))

    def resize(self, screen_constraints: Tuple[int, int]):
        if not self.loaded:
            return
        if self.surface_w != screen_constraints[0] * 2 / 4 or self.surface_h != screen_constraints[1] * 2 / 4:
            self.surface = pg.transform.scale(self.surface, (screen_constraints[0] * 2 / 4, screen_constraints[1] * 2 / 4))
            self.surface_w, self.surface_h = self.surface.get_size()

    def update_timers(self, delta: int):
        self.timer_animal_jump = self.timer_animal_jump - delta
        if self.timer_animal_jump <= 0:
            self.timer_animal_jump = consts.ANIMAL_JUMP_TIME
            self.is_jumping = not self.is_jumping
        if self.is_jumping:
            self.rect.y = self.rect.y - 2
        else:
            self.rect.y = self.rect.y + 2
