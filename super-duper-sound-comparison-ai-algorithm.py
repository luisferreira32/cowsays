from scipy.io import wavfile
from scipy import signal
import numpy as np

# returns a float [0, 100]
def analyzeSound(animal_wav_file_path, silly_human_sound_wav_file_path):
    # Compute FFTs for both audio files
    animal_spectrum = computeFFT(animal_wav_file_path)
    human_spectrum = computeFFT(silly_human_sound_wav_file_path)

    # Get correlation factors
    animal_correlation = signal.correlate(animal_spectrum, animal_spectrum,method='auto', mode='same')
    human_correlation = signal.correlate(human_spectrum, human_spectrum, method='auto', mode='same')
    animal_human_correlation = signal.correlate(animal_spectrum, human_spectrum, method='auto', mode='same')

    animal_max = np.max(animal_correlation) 
    human_max = np.max(human_correlation) 
    animal_human_max = np.max(animal_human_correlation) 

    analysis = animal_human_max**2 / animal_max / human_max

    # Analysis is always between 0.2 and 0.2 so... we do magic
    result = (analysis -0.1)* 10
    result = min(result, 1)
    result = max(result, 0)

    return result
    
def computeFFT(file_path):
    # Read the audio file
    sample_rate, data = wavfile.read(file_path)

    # Get data for the first channel
    # We always dismiss the second channel
    first_channel_data = data[:,0]

    # Compute the magnitude spectrum
    magnitude_spectrum = np.abs(first_channel_data)
    magnitude_spectrum_norm = magnitude_spectrum/np.max(magnitude_spectrum)

    # Compute the FFT
    return np.abs(np.fft.fft(magnitude_spectrum_norm))