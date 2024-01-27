import pygame as pg
from pygame._sdl2 import (
    get_audio_device_names,
    AudioDevice,
    AUDIO_F32,
    AUDIO_ALLOW_FORMAT_CHANGE,
)

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
