from scipy.io import wavfile
from scipy import signal
import numpy as np


# returns an int [0, 100]
def analyze_sound(animal_wav_file_path: str, silly_human_sound_wav_file_path: str) -> int:
    # Compute FFTs for both audio files
    animal_spectrum = compute_fft(animal_wav_file_path)
    human_spectrum = compute_fft(silly_human_sound_wav_file_path)

    # Get correlation factors
    animal_correlation = signal.correlate(animal_spectrum, animal_spectrum, method="auto", mode="same")
    human_correlation = signal.correlate(human_spectrum, human_spectrum, method="auto", mode="same")
    animal_human_correlation = signal.correlate(animal_spectrum, human_spectrum, method="auto", mode="same")

    animal_max = np.max(animal_correlation)
    human_max = np.max(human_correlation)
    animal_human_max = np.max(animal_human_correlation)

    analysis = animal_human_max**2.0 / animal_max / human_max

    # Analysis is always between 0.2 and 0.3 so... we do magic
    result = (analysis - 0.2) * 10.0
    print(f"analysis: {analysis}, uncapped result: {result},")
    result = min(result, 1.0)
    result = max(result, 0.2)

    if result != result:  # NaN check
        result = 0.0

    return int(100 * result)


def compute_fft(file_path):
    # Read the audio file
    _, data = wavfile.read(file_path)

    # Get data for the first channel
    first_channel_data = data
    # We always dismiss the second channel if recording 2 channels
    if len(data.shape) > 1:
        first_channel_data = data[:, 0]

    # Compute the magnitude spectrum
    magnitude_spectrum = np.abs(first_channel_data)
    magnitude_spectrum_norm = magnitude_spectrum / np.max(magnitude_spectrum)

    # Compute the FFT
    return np.abs(np.fft.fft(magnitude_spectrum_norm))
