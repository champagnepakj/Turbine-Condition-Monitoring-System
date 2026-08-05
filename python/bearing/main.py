from detector import detection
from analysis import envelope_analysis
import numpy as np
from config import shaft_speed, freqs
from visualisations import visualise_time_domain_envelope_plot, visualise_envelope_frequency_spectrum
from generate import generate_exponentially_decaying_sin_wave

data = np.load('python/data/cwru/1797_OR@6_7_DE12.npz')
data = data['DE'].flatten()
#print(data)


plain_noise = np.random.normal(0, 0.2, int(20e3))
test_freq, test_mags, test_filt, test_env = envelope_analysis(plain_noise, sample_rate=20e3)
half = len(test_freq) // 2
detection(test_freq[:half], test_mags[:half], freqs.BPFO, shaft_speed, 10)
visualise_time_domain_envelope_plot(plain_noise, test_filt, test_env)
visualise_envelope_frequency_spectrum(test_freq, test_mags, freqs.BPFO)


signal = generate_exponentially_decaying_sin_wave(freqs.BPFO, 20e3, shaft_speed, 0.2)
freqs_axis, mags, filt, env = envelope_analysis(signal, sample_rate=20e3)
half = len(freqs_axis) // 2
detection(freqs_axis[:half], mags[:half], freqs.BPFO, shaft_speed, 10)
visualise_time_domain_envelope_plot(signal, filt, env)
visualise_envelope_frequency_spectrum(freqs_axis, mags, freqs.BPFO)


real_freqs_axis, real_mags, real_filt, real_env = envelope_analysis(data, sample_rate=12e3)
half = len(real_freqs_axis) // 2
detection(real_freqs_axis[:half], real_mags[:half], freqs.BPFO, shaft_speed, 10)
visualise_time_domain_envelope_plot(data, real_filt, real_env)
visualise_envelope_frequency_spectrum(real_freqs_axis, real_mags, freqs.BPFO)
