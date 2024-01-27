import pygame as pg
import time

from typing import Tuple, List

from pygame._sdl2 import (
    get_audio_device_names,
    AudioDevice,
    AUDIO_F32,
    AUDIO_ALLOW_FORMAT_CHANGE,
)

# Screen related sizes
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = tuple([1800, 1200])

# Color palet
BACKGROUND_COLOR = (100, 200, 100)
FONT_COLOR = (0, 0, 0)

# Game pages
PAGE_SHOW_THE_ANIMAL_SAYS = 0
PAGE_SHOW_THE_ANIMAL_RECORDING = 1
PAGE_SHOW_THE_ANIMAL_SCORE = 2


class Recorder:
    def __init__(self):
        names = get_audio_device_names(True)
        self.sound_chunks = []

        def callback(_: AudioDevice, audiomemoryview: memoryview):
            self.sound_chunks.append(bytes(audiomemoryview))

        self.audio_device = AudioDevice(
            devicename=names[0],
            iscapture=True,
            frequency=44100,
            audioformat=AUDIO_F32,
            numchannels=2,
            chunksize=512,
            allowed_changes=AUDIO_ALLOW_FORMAT_CHANGE,
            callback=callback,
        )
        self.recording = False

    def start_recording(self):
        if self.recording:
            return
        self.recording = True
        print("started recording")
        self.audio_device.pause(0)

    def stop_recording(self):
        if not self.recording:
            return
        self.recording = False
        print("paused recording")
        self.audio_device.pause(1)

    def mix_sound(self) -> pg.mixer.Sound:
        return pg.mixer.Sound(buffer=b"".join(self.sound_chunks))


class Animal:
    def __init__(self, name: str, surface: pg.Surface, background_color: pg.Color, foreground_color: pg.Color):
        self.name = name
        self.surface = surface
        self.surface_w, self.surface_h = surface.get_size()
        self.background_color = background_color
        self.foreground_color = foreground_color


class GameState:
    def __init__(self, recorder: Recorder, animal_assets_src: List[str], animal_characteristics: List[Tuple[str, pg.Color, pg.Color]]):
        self.recorder = recorder
        self.animal_assets_src = animal_assets_src
        # TODO: this does not feel right to be a tuple
        self.animal_characteristics = animal_characteristics

        self.current_page = PAGE_SHOW_THE_ANIMAL_SAYS
        self.current_animal = self.next_animal()

        # TODO: keep track of similarities > 60%
        self.score = 0
        # TODO: calculate this when you stop recording
        self.current_evaluation = 0

    def next_animal(self) -> Animal:
        next_animal_asset, next_animal_characteristics = self.animal_assets_src.pop(), self.animal_characteristics.pop()
        next_animal_surface = pg.image.load(next_animal_asset)
        next_animal = Animal(next_animal_characteristics[0], next_animal_surface, next_animal_characteristics[1], next_animal_characteristics[2])
        if next_animal.surface_w != SCREEN_WIDTH * 2 / 4 or next_animal.surface_h != SCREEN_HEIGHT * 2 / 4:
            next_animal.surface = pg.transform.scale(next_animal.surface, (SCREEN_WIDTH * 2 / 4, SCREEN_HEIGHT * 2 / 4))
        self.current_animal = next_animal
        return next_animal


def draw_page_show_the_animal_says(screen: pg.Surface, global_game_state: GameState):
    animal = global_game_state.current_animal
    screen.fill(animal.background_color)
    screen.blit(animal.surface, (SCREEN_WIDTH * 1 / 4, SCREEN_HEIGHT * 1 / 4))

    record_text = font.render(f"The {animal.name} says...", True, FONT_COLOR)
    record_rect = record_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100))
    screen.blit(record_text, record_rect)


def draw_page_show_the_animal_recording(screen: pg.Surface, global_game_state: GameState):
    animal = global_game_state.current_animal
    screen.fill(animal.background_color)
    screen.blit(animal.surface, (SCREEN_WIDTH * 1 / 4, SCREEN_HEIGHT * 1 / 4))

    record_text = font.render(f"Recording your {animal.name} sound", True, FONT_COLOR)
    record_rect = record_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100))
    screen.blit(record_text, record_rect)


def draw_page_show_the_animal_score(screen: pg.Surface, global_game_state: GameState):
    animal = global_game_state.current_animal
    screen.fill(animal.background_color)
    screen.blit(animal.surface, (SCREEN_WIDTH * 1 / 4, SCREEN_HEIGHT * 1 / 4))

    record_text = font.render(f"Your similarity with the {animal.name} is: {global_game_state.current_evaluation}%", True, FONT_COLOR)
    record_rect = record_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100))
    screen.blit(record_text, record_rect)


draw_page_map = {
    PAGE_SHOW_THE_ANIMAL_SAYS: draw_page_show_the_animal_says,
    PAGE_SHOW_THE_ANIMAL_RECORDING: draw_page_show_the_animal_recording,
    PAGE_SHOW_THE_ANIMAL_SCORE: draw_page_show_the_animal_score,
}


def main_game_loop():
    # TODO: dynamically load assets and unload them as we move between animals?
    # TODO: have the colors also in some sort of config file
    global_game_state = GameState(Recorder(), ["tmp/cow.webp"], [("cow", BACKGROUND_COLOR, FONT_COLOR)])

    # TODO: figure something else to do "real-time" fps independent timers
    recording_time = 0
    while True:
        # process events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                the_jam = global_game_state.recorder.mix_sound()
                the_jam.play()
                # time.sleep(5)
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                global_game_state.recorder.start_recording()
                global_game_state.current_page = PAGE_SHOW_THE_ANIMAL_RECORDING
                # TODO: don't use this variable, figure out something else ?
                recording_time = 5000

        # draw stuff
        draw_page_map[global_game_state.current_page](screen, global_game_state)
        pg.display.flip()

        # handle real-time calculations
        delta_ms = clock.tick(60)
        if recording_time > 0:
            recording_time -= delta_ms
        if recording_time < 0:
            global_game_state.recorder.stop_recording()
            recording_time = 0
            global_game_state.current_page = PAGE_SHOW_THE_ANIMAL_SCORE


pg.mixer.pre_init(44100, 32, 2, 512)
pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
font = pg.font.SysFont("Mono", 50)

main_game_loop()
pg.quit()
