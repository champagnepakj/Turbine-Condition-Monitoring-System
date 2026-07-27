from geometry import Bearing, fault_frequencies
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, fft
from scipy.fft import fftfreq

cwru_bearing = Bearing("CWRU 6205",
               9,
               7.94,
               39.04,
               contact_angle=0.0)

freqs = fault_frequencies(cwru_bearing, 1.0)

sample_rate = 20e3 # 20,000 Hz
decay = 700 # need to twqeak this between 700-1000


fImpact = 3500 # 3.5 kHz
#tImpact = np.arange(0, 5e-3, 1/sample_rate) # start at 0, stop at 5 miliseconds(0.005s), step by 1/20,000

tImpact = np.arange(0, 5e-3, 1/sample_rate) # start at 0, stop at 5 miliseconds(0.005s), step by 1/20,000
xImpact = np.sin(2 * np.pi * fImpact * tImpact) * np.exp(-decay * tImpact)

duration = 50.0
t = np.arange(0, duration, 1 / sample_rate)
raw_signal = np.zeros(len(t))
noise = np.random.default_rng(seed=42).normal(0, 0.05, len(raw_signal))
raw_signal = raw_signal + noise
impact_spacing = int(sample_rate / freqs.BPFO)

for start in range(0, len(raw_signal), impact_spacing):
    end = start + len(xImpact)
    if end <= len(raw_signal):
        raw_signal[start:end] += xImpact

'''
plt.plot(t, raw_signal)
plt.xlim([0.25, 0.3])
plt.title("Local Fault Impacts on Bearing")
plt.xlabel("Time (s)")
plt.ylabel("Acceleration (m/s^2)")
plt.show()
'''

sos = signal.butter(4, [2000, 5000], 'bandpass', fs=sample_rate, output='sos')
filtered = signal.sosfilt(sos, raw_signal)
envelope = np.abs(signal.hilbert(filtered))

#spectrum = np.abs(np.fft.rfft(envelope))
spectrum = np.abs(np.fft.rfft(envelope - np.mean(envelope)))
freqs_axis = np.fft.rfftfreq(len(envelope), 1/sample_rate)

plt.figure()
plt.plot(freqs_axis, spectrum)
plt.xlim([0, 50])
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.title("Envelope spectrum")
plt.show()

mask = (freqs_axis > 2) & (freqs_axis < 5)
peak_idx = np.where(mask)[0][np.argmax(spectrum[mask])]
print(f"Peak near BPFO: {freqs_axis[peak_idx]:.2f} Hz")
print(f"Expected BPFO: {freqs.BPFO:.2f} Hz")

'''
plt.plot(t, filtered, linewidth=0.5, color='black')
plt.plot(t, raw_signal, color='purple', alpha=0.4)
plt.plot(t, envelope, color='red')
plt.plot(transformed_x, np.abs(transformed_y))
#plt.xlim([0.25, 0.3])
plt.xlim([-0.1, 1.0])
plt.title("Local Fault Impacts on Bearing Filtered")
plt.xlabel("Time (s)")
plt.ylabel("Acceleration (m/s^2)")
plt.show()
'''
