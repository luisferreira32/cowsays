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
BACKGROUND_COLOR = (100,200,100)
FONT_COLOR = (0,0,0)

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
        self.animal_characteristics = animal_characteristics
        self.timer_begin = time.time()
        self.record = True

        self.current_screen = "page_show_the_animal"

        first_animal_asset, first_animal_characteristics = self.animal_assets_src.pop(), self.animal_characteristics.pop()
        first_animal_surface = pg.image.load(first_animal_asset)
        self.current_animal = Animal(first_animal_characteristics[0], first_animal_surface, first_animal_characteristics[1], first_animal_characteristics[2])
    
    def next_animal(self) -> Animal:
        first_animal_asset, first_animal_characteristics = self.animal_assets_src.pop(), self.animal_characteristics.pop()
        first_animal_surface = pg.image.load(first_animal_asset)
        self.current_animal = Animal(first_animal_characteristics[0], first_animal_surface, first_animal_characteristics[1], first_animal_characteristics[2])
        return self.current_animal


def draw_page_show_the_animal(screen : pg.Surface, global_game_state : GameState):
    animal = global_game_state.current_animal
    screen.fill(animal.background_color)

    if animal.surface_w != SCREEN_WIDTH*2/4 or animal.surface_h != SCREEN_HEIGHT*2/4:
        animal.surface = pg.transform.scale(animal.surface, (SCREEN_WIDTH*2/4, SCREEN_HEIGHT*2/4))
    screen.blit(animal.surface, (SCREEN_WIDTH*1/4, SCREEN_HEIGHT*1/4))

    record_text = font.render(f"The {animal.name} says...", True, FONT_COLOR)
    record_rect = record_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-100))
    screen.blit(record_text, record_rect)

    if global_game_state.record:
        global_game_state.recorder.start_recording()
        # record for 5 seconds
        if (time.time() - global_game_state.timer_begin) > 5:
            global_game_state.record = False
        pg.draw.circle(screen, "red", (record_rect.right+40, record_rect.centery-20), 20.0, width=3)
    else:
        global_game_state.recorder.stop_recording()
        pg.draw.circle(screen, FONT_COLOR, (record_rect.right+40, record_rect.centery-20), 20.0, width=3)


def main_game_loop():
    global_game_state = GameState(Recorder(), ["tmp/cow.webp"], [("cow", BACKGROUND_COLOR, FONT_COLOR)])

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                the_jam = global_game_state.recorder.mix_sound()
                the_jam.play()
                time.sleep(5)
                return

        if global_game_state.current_screen == "page_show_the_animal":
            draw_page_show_the_animal(screen, global_game_state)

        pg.display.flip()

        clock.tick(60)  # limits FPS to 60


pg.mixer.pre_init(44100, 32, 2, 512)
pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
font = pg.font.SysFont("Mono", 50)

main_game_loop()
pg.quit()