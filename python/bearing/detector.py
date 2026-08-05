from scipy import signal
from scipy.signal import find_peaks


def detection(final_signal, fft_signal, fault_type, shaft_speed, loop_length):
     detections = []
     harmonic = fault_type * shaft_speed
     peak_indices, properties = signal.find_peaks(fft_signal, prominence=100)

     for i in range(1, loop_length):
          target_freq = harmonic * i
          tolerance = target_freq * 0.02

          for idx in peak_indices:
               if abs(final_signal[idx] - target_freq) <= tolerance:
                    detections.append({"frequency": target_freq, "magnitude": fft_signal[idx]})
                    print(f"Anomaly detected at frequency {target_freq:.1f}Hz, magnitude {fft_signal[idx]:.1f}")
                    break

     return detections
