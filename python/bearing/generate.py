from geometry import Bearing, fault_frequencies
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fft import fftfreq, fft
import math

cwru_bearing = Bearing("CWRU 6205",
               9,
               7.94,
               39.04,
               contact_angle=0.0)

freqs = fault_frequencies(cwru_bearing, 1.0)

'''
# freqs = 
# BPFO  = 3.584784836065573,
# BPFI  = 5.415215163934427,
# FTF   = 0.39830942622950816,
# BSF   = 2.3567477133831605
'''

sample_rate_hz = 20e3 # 20,000 Hz / 20 kHz
fImpact = 3000
decay = 1000
shaft_speed = 30
# harmonic = 107.5 # the intervals to check peaks, FOR BPFO
# points per cycle = 20e3/3000 = 6.67 points
# total ringing duration = 5/decay constant = 5/1000 = 0.005seconds (5ms)

# decay window samples = 0.005 s * 20e3 Hz = 100 samples:
#   this means that every a ball strikes the defect, the system will
#   ring smoothly for exactly 100 data points before falling silent

# the gap between impulses (in the array) is calculated by sample_rate/fault/freq

signal_duration = np.zeros(20000)
window = 5 / decay
num_samples = int(round(window * sample_rate_hz))
t = np.linspace(0, window, num_samples)

value = ((np.exp(-decay * t))) * np.sin(2 * math.pi * t * fImpact)
step = sample_rate_hz / (freqs.BPFO * shaft_speed)

for i in range(0, len(signal_duration), int(round(step))):
    end = min(i + len(value), len(signal_duration))
    signal_duration[i:end] = value[:end - i ]

# add the gaussian white noise
signal_duration += np.random.normal(loc=0, scale=0.2, size=20000)

def envelope_analysis(input_signal, sample_rate):
    # apply a bandpass filter, butterworth
    bandpass_signal = signal.butter(4, Wn=(2000, 4000), btype='bandpass', fs=sample_rate, output='sos')
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


#final_freqs, magnitudes, filt, env = envelope_analysis(signal_duration, sample_rate_hz)



def detection(final_signal, fft_signal, harmonic, loop_length):
    for i in range(1, loop_length, 1):
        target_freq = harmonic * i
        idx = np.argmin(np.abs(final_signal-target_freq))
        scanned_magnitude = fft_signal[idx]
        err_message = f"Anomally detected at frequency {target_freq}Hz, of magnitude {scanned_magnitude}"

        window_size = 20
        guard_bins = 2
        left_noise = fft_signal[idx - window_size : idx - guard_bins]
        right_noise = fft_signal[idx + guard_bins + 1 : idx + window_size + 1]
        local_noise = np.concatenate([left_noise, right_noise])

        local_mean = np.mean(local_noise)
        local_std = np.std(local_noise)
        threshold = local_mean + 5 * local_std

        if scanned_magnitude > threshold:
            print(err_message)
        else:
            print("None")



plain_noise = np.random.normal(0, 0.2, 20000)

        


#detection(final_freqs[:1000], magnitudes[:1000], 107.5, 10)

test_freq, test_mag, test_filt, test_env = envelope_analysis(plain_noise, sample_rate_hz)
detection(test_freq, test_mag, 107.5, 10)

plt.figure()
plt.plot(plain_noise[:1000])
plt.plot(test_filt[:1000])
plt.plot(test_env[:1000], color='red')
#plt.plot(signal_duration[:1000])
#plt.plot(filt[:1000])
#plt.plot(env[:1000], color='red')
plt.xlabel('Samples')
plt.ylabel('Acceleration')
plt.show()


plt.figure()
#plt.plot(final_freqs[:1000], magnitudes[:1000])
plt.plot(test_freq[:1000], test_mag[:1000])
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')

for i in range (1, 10):
    plt.axvline(x=107.5 * i, color='black', linestyle='--')
plt.show()


