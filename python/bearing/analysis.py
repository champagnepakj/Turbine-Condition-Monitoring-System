from scipy import signal
from scipy.fft import fft
import numpy as np



def envelope_analysis(input_signal, sample_rate):
    # apply a bandpass filter, butterworth
    bandpass_signal = signal.butter(4, Wn=(3000, 4000), btype='bandpass', fs=sample_rate, output='sos')
    # integrate the filter onto the original signal
    filtered_signal = signal.sosfiltfilt(sos=bandpass_signal, x=input_signal)
    # hilbert transform
    hilbert_signal = signal.hilbert(filtered_signal)
    envelope_signal = np.abs(hilbert_signal)
    mean_data = np.mean(envelope_signal)    # calculate the mean of the signal subtract
    envelope_signal -= mean_data            # the mean to remove DC peak at 0Hz
    fft_signal = abs(fft(envelope_signal))  # magnitudes
    final_signal = np.fft.fftfreq(n=len(input_signal), d=1/sample_rate) # frequencies

    return final_signal, fft_signal, filtered_signal, envelope_signal
