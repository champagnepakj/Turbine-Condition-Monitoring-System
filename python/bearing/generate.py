from geometry import Bearing, fault_frequencies
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import find_peaks
from scipy.fft import fftfreq, fft
import math
from detector import detection
from analysis import envelope_analysis
from config import decay, fImpact, duration_seconds



'''
# freqs = 
# BPFO  = 3.584784836065573,
# BPFI  = 5.415215163934427,
# FTF   = 0.39830942622950816,
# BSF   = 2.3567477133831605
'''

#sample_rate_hz = 12e3 # 20,000 Hz / 20 kHz
#fImpact = 3000
#decay = 1000
#shaft_speed = 29.95
# harmonic = 107.5 # the intervals to check peaks, FOR BPFO
# points per cycle = 20e3/3000 = 6.67 points
# total ringing duration = 5/decay constant = 5/1000 = 0.005seconds (5ms)

# decay window samples = 0.005 s * 20e3 Hz = 100 samples:
#   this means that every a ball strikes the defect, the system will
#   ring smoothly for exactly 100 data points before falling silent

# the gap between impulses (in the array) is calculated by sample_rate/fault/freq

'''
signal_duration = np.zeros(20000)
window = 5 / decay
num_samples = int(round(window * sample_rate_hz))
t = np.linspace(0, window, num_samples)

value = ((np.exp(-decay * t))) * np.sin(2 * math.pi * t * fImpact)
step = sample_rate_hz / (freqs.BPFO * shaft_speed)
#step = sample_rate_hz / (freqs.BPFI * shaft_speed)
#step = sample_rate_hz / (freqs.FTF * shaft_speed)


for i in range(0, len(signal_duration), int(round(step))):
    end = min(i + len(value), len(signal_duration))
    signal_duration[i:end] = value[:end - i]

# add the gaussian white noise
signal_duration += np.random.normal(loc=0, scale=0.2, size=20000)
'''


def generate_exponentially_decaying_sin_wave(fault_type, sample_rate, shaft_speed, noise_scale):
    signal_duration = np.zeros(int(sample_rate * duration_seconds))
    window = 5 / decay
    num_samples = int(round(window * sample_rate))
    t = np.linspace(0, window, num_samples)

    value = ((np.exp(-decay * t))) * np.sin(2 * math.pi * t * fImpact)
    step = sample_rate / (fault_type * shaft_speed)

    for i in range(0, len(signal_duration), int(round(step))):
        end = min(i + len(value), len(signal_duration))
        signal_duration[i:end] = value[:end - i]

    signal_duration += np.random.normal(loc=0, scale=noise_scale, size=len(signal_duration))

    return signal_duration











