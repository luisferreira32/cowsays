import pyaudio
import wave, sys

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 # 1 channel is more likely to be supported
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"


class Recorder:
    def __init__(self):
        self.port_audio = pyaudio.PyAudio()
        self.recording = False
        self.sound_chunks = []

    def start_recording(self):
        if self.recording:
            return
        self.recording = True
        print("started recording")

        wav_file = wave.open(WAVE_OUTPUT_FILENAME, "wb")
        wav_file.setnchannels(CHANNELS)
        wav_file.setsampwidth(self.port_audio.get_sample_size(FORMAT))
        wav_file.setframerate(RATE)
        self.wav_file = wav_file

        def callback(in_data: bytes, frame_count, time_info, status):
            wav_file.writeframes(in_data)
            return (in_data, pyaudio.paContinue)

        self.stream = self.port_audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, stream_callback=callback)

    def stop_recording(self):
        if not self.recording:
            return
        self.recording = False
        print("stopped recording")

        self.stream.stop_stream()
        self.stream.close()

        self.wav_file.close()
