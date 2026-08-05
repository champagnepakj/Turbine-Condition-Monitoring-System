import matplotlib.pyplot as plt
#from main import plain_noise, test_filt, test_env, test_freq, test_mag


def visualise_time_domain_envelope_plot(signal, filtered_signal, envelope):
    plt.figure()
    plt.plot(signal[:1000])
    plt.plot(filtered_signal[:1000])
    plt.plot(envelope[:1000], color='red')
    plt.xlabel('Samples')
    plt.ylabel('Acceleration')
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
