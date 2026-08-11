import matplotlib.pyplot as plt
#from main import plain_noise, test_filt, test_env, test_freq, test_mag
import numpy as np

plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams.update({
    'figure.figsize': (12, 4),
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'figure.dpi': 150
})

def visualise_time_domain_envelope_plot(signal, filtered_signal, envelope, sample_rate):
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.figure(figsize=(12, 4), dpi=150)
    
    time_axis = np.arange(1000) / sample_rate
    
    plt.plot(time_axis, signal[:1000], alpha=0.5, label='Raw signal')
    plt.plot(time_axis, filtered_signal[:1000], alpha=0.7, label='Bandpass filtered')
    plt.plot(time_axis, envelope[:1000], color='red', linewidth=2, label='Envelope')
    
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (g)')
    plt.title('Bearing Defect Signal - Time Domain with Envelope')
    plt.legend()
    plt.tight_layout()
    plt.savefig('docs/images/time_domain_envelope_high.png', bbox_inches='tight')
    plt.show()

def visualise_envelope_frequency_spectrum(frequency, magnitude, fault_type, shaft_speed):
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.figure(figsize=(12, 4), dpi=150)
    
    half = len(frequency) // 2
    plt.plot(frequency[:half], magnitude[:half], linewidth=1)
    plt.xlim(0, 1000)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.title('Envelope Spectrum - BPFO Harmonic Detection')

    harmonic_freq = fault_type * shaft_speed
    for i in range(1, 10):
        plt.axvline(x=harmonic_freq * i, color='red', linestyle='--', alpha=0.3,
                    label=f'{i}× BPFO' if i <= 3 else None)

    plt.legend()
    plt.tight_layout()
    plt.savefig('docs/images/envelope_spectrum_high.png', bbox_inches='tight')
    plt.show()

'''
def visualise_time_domain_envelope_plot(signal, filtered_signal, envelope):
    plt.figure()
    plt.plot(signal[:1000])
    plt.plot(filtered_signal[:1000])
    plt.plot(envelope[:1000], color='red')
    plt.xlabel('Samples')
    plt.ylabel('Acceleration')
    plt.tight_layout()
    plt.savefig('docs/images/impulse_train.png', bbox_inches='tight')
    plt.show()

def visualise_envelope_frequency_spectrum(frequency, magnitude, fault_type):
    plt.figure()
    plt.xlim(0, 1000)
    half = len(frequency) // 2
    plt.plot(frequency[:half], magnitude[:half])
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')

    for i in range (1, 10):
        #plt.axvline(x=107.5 * i, color='black', linestyle='--')
        plt.axvline(x=fault_type * 29.95 * i, color='black', linestyle='--')

    plt.show()

'''


'''
plt.figure()
plt.plot(plain_noise[:1000])
plt.plot(test_filt[:1000])
plt.plot(test_env[:1000], color='red')
plt.xlabel('Samples')
plt.ylabel('Acceleration')
plt.show()
'''

'''
plt.figure()
plt.plot(test_freq[:1000], test_mag[:1000])
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')

for i in range (1, 10):
    plt.axvline(x=107.5 * i, color='black', linestyle='--')
plt.show()
'''


'''
for i in range (1, 10):
    x = freqs.BPFO * shaft_speed
    plt.axvline(x=x * i, color='black', linestyle='--')
plt.show()
'''

'''
plt.figure()
plt.plot(signal_duration[:1000])
plt.plot(filt[:1000])
plt.plot(env[:1000], color='red')
plt.xlabel('Samples')
plt.ylabel('Acceleration')
plt.show()
'''


'''
plt.figure()
raw_fft = np.abs(np.fft.fft(data))
freqs = np.fft.fftfreq(len(data), d=1/12000)
half = len(freqs) // 2
plt.plot(freqs[:half], raw_fft[:half])
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.show()
'''
'''
plt.figure()
half = len(final_freqs) // 2
#plt.plot(final_freqs[:1000], magnitudes[:1000])
plt.plot(final_freqs[:half], magnitudes[:half])
plt.xlim(50,200)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
'''
