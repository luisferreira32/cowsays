import pygame as pg
import time

from pygame._sdl2 import (
    get_audio_device_names,
    AudioDevice,
    AUDIO_F32,
    AUDIO_ALLOW_FORMAT_CHANGE,
)
from pygame._sdl2.mixer import set_post_mix

pg.mixer.pre_init(44100, 32, 2, 512)
# pg setup
pg.init()

screen = pg.display.set_mode((1800, 1200))

clock = pg.time.Clock()

cowimg = pg.image.load("tmp/cow.webp")


font = pg.font.SysFont("Arial", 50)
record_text = font.render(" RECORD ", True, (255, 255, 255), (0, 0, 0))
record_rect = record_text.get_rect(topleft=(900,1100))

score_text = font.render(" 0% ", True, (255, 255, 255), (0, 0, 0))
score_rect = record_text.get_rect(topleft=(900,1100))

# init_subsystem(INIT_AUDIO)
names = get_audio_device_names(True)
print(names)

sounds = []
sound_chunks = []

def callback(audiodevice, audiomemoryview):
    """This is called in the sound thread.

    Note, that the frequency and such you request may not be what you get.
    """
    # print(type(audiomemoryview), len(audiomemoryview))
    # print(audiodevice)
    sound_chunks.append(bytes(audiomemoryview))



audio = AudioDevice(
    devicename=names[0],
    iscapture=True,
    frequency=44100,
    audioformat=AUDIO_F32,
    numchannels=2,
    chunksize=512,
    allowed_changes=AUDIO_ALLOW_FORMAT_CHANGE,
    callback=callback,
)

display_score = False

def on_mouse_button_down(event):
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and record_rect.collidepoint(event.pos):
        # start recording.
        audio.pause(0) # INDEFINETLY!!!
        print(f"recording with '{names[0]}'")
        time.sleep(5)
        print("Turning data into a pg.mixer.Sound")
        sound = pg.mixer.Sound(buffer=b"".join(sound_chunks))
        print("playing back recorded sound")
        globals()["display_score"] = True
        sound.play()
        # time.sleep(5)

def gameloop():
    while True:
        # poll for events
        # pg.QUIT event means the user clicked X to close your window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            
            # Check for the mouse button down event
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                # Call the on_mouse_button_down() function
                on_mouse_button_down(event)

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")
        screen.blit(cowimg, (20, 20))
        if display_score:
            screen.blit(score_text, score_rect)
        else:
            screen.blit(record_text, record_rect)

        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        pg.display.flip()

        clock.tick(60)  # limits FPS to 60


gameloop()
pg.quit()