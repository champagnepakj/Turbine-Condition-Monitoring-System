import pytest
from generate import generate_exponentially_decaying_sin_wave
from analysis import envelope_analysis
from detector import detection
from config import freqs

import numpy as np

data = np.load('python/data/cwru/1797_OR@6_7_DE12.npz')
data = data['DE'].flatten()

def test_noise_BPFO():
    plain_noise = np.random.normal(0, 0.2, int(20e3))
    test_freq, test_mags, test_filt, test_env = envelope_analysis(plain_noise, sample_rate=20e3)
    half = len(test_freq) // 2
    output = detection(test_freq[:half], test_mags[:half], freqs.BPFO, 29.95, 10)

    assert not output

def test_generated_signal_BPFO():
    signal = generate_exponentially_decaying_sin_wave(freqs.BPFO, 20e3, 29.95, 0.2)
    freqs_axis, mags, filt, env = envelope_analysis(signal, sample_rate=20e3)
    half = len(freqs_axis) // 2
    output = detection(freqs_axis[:half], mags[:half], freqs.BPFO, 29.95, 10)

    assert abs(output[0]['frequency'] - freqs.BPFO * 29.95) < 2.0
    assert len(output) > 0

def test_real_signal_BPFO():
    real_freqs_axis, real_mags, real_filt, real_env = envelope_analysis(data, sample_rate=12e3)
    half = len(real_freqs_axis) // 2
    output = detection(real_freqs_axis[:half], real_mags[:half], freqs.BPFO, 29.95, 10)

    assert abs(output[0]['frequency'] - freqs.BPFO * 29.95) < 2.0
    assert len(output) > 0

def test_generated_signal_BPFI():
    signal = generate_exponentially_decaying_sin_wave(freqs.BPFI, 20e3, 29.95, 0.2)
    freqs_axis, mags, filt, env = envelope_analysis(signal, sample_rate=20e3)
    half = len(freqs_axis) // 2
    output = detection(freqs_axis[:half], mags[:half], freqs.BPFI, 29.95, 10)

    assert abs(output[0]['frequency'] - freqs.BPFI * 29.95) < 2.0
    assert len(output) > 0

def test_generated_signal_BSF():
    signal = generate_exponentially_decaying_sin_wave(freqs.BSF, 20e3, 29.95, 0.2)
    freqs_axis, mags, filt, env = envelope_analysis(signal, sample_rate=20e3)
    half = len(freqs_axis) // 2
    output = detection(freqs_axis[:half], mags[:half], freqs.BSF, 29.95, 10)

    assert abs(output[0]['frequency'] - freqs.BSF * 29.95) < 2.0
    assert len(output) > 0

def test_generated_signal_FTF():
    signal = generate_exponentially_decaying_sin_wave(freqs.FTF, 20e3, 29.95, 0.2)
    freqs_axis, mags, filt, env = envelope_analysis(signal, sample_rate=20e3)
    half = len(freqs_axis) // 2
    output = detection(freqs_axis[:half], mags[:half], freqs.FTF, 29.95, 10)

    #assert abs(output[0]['frequency'] - freqs.FTF * 29.95) < 2.0
    assert len(output) > 0
