import pygame as pg
from typing import Tuple

class Animal:
    def __init__(self, name: str, asset_src: str, background_color: pg.Color, foreground_color: pg.Color):
        self.name = name
        self.asset_src = asset_src
        self.surface_w, self.surface_h = 0, 0
        self.background_color = background_color
        self.foreground_color = foreground_color

    def load_surface(self, screen_constraints: Tuple[int, int]):
        self.surface = pg.image.load(self.asset_src)
        self.surface_w, self.surface_h = self.surface.get_size()
        if self.surface_w != screen_constraints[0] * 2 / 4 or self.surface_h != screen_constraints[1] * 2 / 4:
            self.surface = pg.transform.scale(self.surface, (screen_constraints[0] * 2 / 4, screen_constraints[1] * 2 / 4))
