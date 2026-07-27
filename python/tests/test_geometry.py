import pytest
from python.bearing.geometry import Bearing, fault_frequencies

# Using the CWRU 6205 bearing parameters
# This is the drive-end bearing used in the Case Western Reserve University fault-signature dataset.
# SKF 6205-2RS JEM deep groove ball bearing

# Expected values from CWRU Bearing Data Center
# https://engineering.case.edu/bearingdatacenter
# SKF 6205-2RS JEM, drive end

'''
Parameters:
- Name:             CWRU 6205
- Number of Balls:  9 (n_elements)
- Ball Diameter:    7.49 mm | 0.3126 in (elements_diameter)
- Pitch Diameter:   39.04 mm | 1.5370 in (pitch_diameter)
- Contact Angle:    0 deg
'''

cwru_bearing = Bearing("CWRU 6205",
               9,
               7.94,
               39.04,
               contact_angle=0.0)

def test_BPFO():
    freqs = fault_frequencies(cwru_bearing, shaft_hz=1.0)

    #assert freqs.BPFO == pytest.approx(3.6367, rel=1e-3)
    #assert freqs.BPFI == pytest.approx(5.3633, rel=1e-3)
    #assert freqs.FTF == pytest.approx(0.4041, rel=1e-3)
    #assert freqs.BSF == pytest.approx(2.5102, rel=1e-3)

    assert freqs.BPFO == pytest.approx(3.5848, rel=1e-3)
    assert freqs.BPFI == pytest.approx(5.4152, rel=1e-3)
    assert freqs.FTF == pytest.approx(0.3983, rel=1e-3)
    assert freqs.BSF == pytest.approx(2.3568, rel=1e-3)

    id_one = cwru_bearing.n_elements * 1.0
    id_two = cwru_bearing.n_elements * freqs.FTF

    assert freqs.BPFO + freqs.BPFI == pytest.approx(id_one)
    assert freqs.BPFO == pytest.approx(id_two)
