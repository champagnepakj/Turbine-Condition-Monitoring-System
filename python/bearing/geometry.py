from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Bearing:
    name:               str
    n_elements:         int         # n
    elements_diameter:  float       # d
    pitch_diameter:     float       # D
    contact_angle:      float = 0.0 

@dataclass
class Frequencies:
    BPFO:               float
    BPFI:               float
    FTF:                float
    BSF:                float


def fault_frequencies(bearing: Bearing, shaft_hz: float): # shaft_hz = fr
    # Ballpass Frequency, outer race:
    BPFO = ((bearing.n_elements * shaft_hz) / 2) * (1 - (bearing.elements_diameter / bearing.pitch_diameter * math.cos(bearing.contact_angle)))

    # Ballpass Frequency, inner race:
    BPFI = ((bearing.n_elements * shaft_hz) / 2) * (1 + (bearing.elements_diameter / bearing.pitch_diameter * math.cos(bearing.contact_angle)))
        
    # Fundamental train frequency (cage speed):
    FTF = (shaft_hz / 2 ) * (1 - (bearing.elements_diameter / bearing.pitch_diameter * math.cos(bearing.contact_angle)))

    # Ball (roller) spin frequency:
    BSF = ((bearing.pitch_diameter * shaft_hz) / (bearing.elements_diameter * 2)) * (1 - (bearing.elements_diameter / bearing.pitch_diameter * math.cos(bearing.contact_angle)) ** 2)

    return Frequencies(BPFO=BPFO, BPFI=BPFI, FTF=FTF, BSF=BSF)
